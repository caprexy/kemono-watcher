import constants
import urllib.request
import json
import logging
import sqlite3
import threading

from . import userModel
from inputPanel import statusHelper
from typing import List

cursorList = []
connectionList = []

class Database(object):
    """ Model of a database backed by a sqlite database"""
    def __init__(self):
        logging.info("Creating new database object")
        # gathering cursors and connections to be closed later on
        self.thread_data = threading.local()

        connection, cursor = self.get_connection_and_cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{constants.USERS_TABLE_NAME}'")
        existing_table = cursor.fetchone()

        if existing_table is None:
            cursor.execute(constants.USER_TABLE_QUERY)
            logging.info("Creating new table")
        else:
            logging.info("Found table")

    def get_connection_and_cursor(self)-> (sqlite3.Connection, sqlite3.Cursor): 
        """Checks if the thread_data has a connection yet. Aka if this thread has a connection.
           If not, opens a connection. Attempts to ensure a single connection per thread

        Returns:
            sqlite.Connection: Connection object of thread connection
            sqlite.Cursor: Cursor obj of thread connection
        """
        if not hasattr(self.thread_data, "connection") or self.thread_data.connection is None:
            self.thread_data.connection = sqlite3.connect(constants.DATABASE_FILENAME)
            connectionList.append(self.thread_data.connection)
            self.thread_data.cursor = self.thread_data.connection.cursor()
            cursorList.append(self.thread_data.cursor)
        return self.thread_data.connection, self.thread_data.cursor
    
    def close_thread_connections(self):
        """Close all thread database connections
        """
        if hasattr(self.thread_data, "cursor"):
            cursorList.remove(self.thread_data.cursor)
            self.thread_data.cursor.close()
            self.thread_data.cursor = None
        if hasattr(self.thread_data, "connection"):
            connectionList.remove(self.thread_data.connection)
            self.thread_data.connection.close()
            self.thread_data.connection = None

    def create_user(self, id: int, service: str, addButton, *staticCallbacks):
        """Creates a user in the database, user data should closely follow user_obj

        Args:
            id (int): Id on kemono of the user
            service (str): Service for the id
            addButton (Button): button to be enabled/disabled while this runs
        """
        thread_connection, thread_cursor = self.get_connection_and_cursor()
        try:
            # get ids
            statusHelper.setuserOperationStatusValues("Got 0 user posts", "orange")

            request = "https://kemono.party/api/" + service.lower() + "/user/" + str(id) + "?o="
            i = 0
            known_id_list = []
            statusHelper.setuserOperationStatusValues("Looking for posts",  "orange")
            contents = urllib.request.urlopen(request + str(i)).read()
            response = json.loads(contents.decode())
            while(bool(response)): #keep running while contents exists
                statusHelper.setuserOperationStatusValues("Got " +str(i)+" user posts and looking more",  "orange")
                for obj in response:
                    known_id_list.append(int(obj["id"]))

                i += 50
                contents = urllib.request.urlopen(request + str(i)).read()
                response = json.loads(contents.decode())

            statusHelper.setuserOperationStatusValues("Finished getting all posts",  "orange")

            # actually write the new user and put it into the database
            known_id_list_json = json.dumps(known_id_list)
            unknown_id_list_json = json.dumps([])
            insert_query = f"INSERT INTO {constants.USERS_TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?)"
            data_to_insert = (None, "na", id, service, known_id_list_json, unknown_id_list_json)
            thread_cursor.execute(insert_query, data_to_insert)
            statusHelper.setuserOperationStatusValues("User is now in database, reclick to view",  "green")
            addButton["state"] = "normal"
            thread_connection.commit()
            
            for callback in staticCallbacks:
                callback()
        except Exception as error:
            logging.error("Failed to add a user: %s", {error})
            thread_connection.rollback()
        finally:
            self.close_thread_connections()

    def update_database_row_user_object(self, user_obj:userModel.User):
        """Updates a database row using a user object's info

        Args:
            user_obj (userModel.User): User obj to insert
        """
        logging.info("Updating user: %s", user_obj)
        connection, cursor = self.get_connection_and_cursor()
        row_tuple = user_obj.get_as_row_tuple()
        database_id = row_tuple[0]

        set_clause = ", ".join(f"{column} = ?" for column in constants.USER_TABLE_COL_NAMES[1:])
        update_query = f"UPDATE {constants.USERS_TABLE_NAME} SET {set_clause} WHERE {constants.USER_TABLE_COL_NAMES[0]} = ?"
        values = row_tuple[1:] + (database_id,)

        cursor.execute(update_query, values)
        connection.commit()

    def update_database_row_manual_input(self, user_id: int, service: str, known_ids: List[int], unknown_ids:List[int]):
        """Alternative way to update the database in the case we know minimal user info + new values to update

        Args:
            user_id (int): _description_
            service (str): _description_
            known_ids (List[int]): _description_
            unknown_ids (List[int]): _description_

        Raises:
            ValueError: _description_
        """
        user_obj = self.get_user_obj(user_id,service)
        if user_obj is None:
            raise ValueError("Couldnt find a user object")
        user_obj.checked_post_ids = known_ids
        user_obj.unchecked_post_ids = unknown_ids 
        self.update_database_row_user_object(user_obj)

    def delete_user(self, user_id: int, service: str, *staticCallbacks):
        """Deletes a user with minimal info

        Args:
            user_id (int): id of user
            service (str): service of user
        """
        connection, cursor = self.get_connection_and_cursor()
        try:    
            delete_query = f"DELETE FROM {constants.USERS_TABLE_NAME} WHERE {constants.USER_TABLE_COL_NAMES[2]} = ? AND {constants.USER_TABLE_COL_NAMES[3]} = ?"
            cursor.execute(delete_query, (user_id, service))
            connection.commit()
            statusHelper.setuserOperationStatusValues("Deleted user", "green")

            for callback in staticCallbacks:
                callback()
        except Exception as error:
            logging.error("Failed to delete a user: %s", error)
            statusHelper.setuserOperationStatusValues("Failed to delete user", "red")
            connection.rollback()
        finally:
            self.close_thread_connections()

    # various gets
    def get_all_uknown_post_ids_and_service(self)-> list[str]:
        """Gets all unknown post, ids, and services from the entirety of the database and services 
        (in the case two post ids can be the same id but different service)

        Returns:
            list[str]: is a list of strings where the string is in the format "post id, service, id"
        """
        connection, cursor = self.get_connection_and_cursor()

        select_query = f"SELECT {constants.USER_TABLE_COL_NAMES[5]},{constants.USER_TABLE_COL_NAMES[3]},{constants.USER_TABLE_COL_NAMES[2]} FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        unknown_posts = []
        for row in rows:
            for post_id in json.loads(row[0]):
                unknown_posts.append(f"{post_id},{row[1]},{row[2]}")

        return unknown_posts
    
    def does_user_exist(self, user_id: int, service: str)-> bool:
        """checks for user

        Args:
            user_id (int): user id
            service (str): user service

        Returns:
            bool: if exist or not
        """
        return bool(self.get_user_obj(user_id, service))
    
    def get_user_obj(self, user_id: int, service: str)->userModel.User:
        """gets the user object from id + service

        Args:
            user_id (int): user id
            service (str): user service

        Returns:
            userModel.User: user object
        """
        connection, cursor = self.get_connection_and_cursor()

        select_query = f"SELECT * FROM {constants.USERS_TABLE_NAME} WHERE {constants.USER_TABLE_COL_NAMES[2]} = ? AND {constants.USER_TABLE_COL_NAMES[3]} = ?"
        cursor.execute(select_query, (user_id, service))

        row = cursor.fetchone()
        # maybe more efficent way of checking if user exist
        if row is None: 
            return None

        return userModel.convert_row_to_user(row)

    def get_all_user_obj(self)->List[userModel.User]:
        """Gets all users in the form of a user model

        Returns:
            List[userModel.User]: contains all user objects registered
        """
        connection, cursor = self.get_connection_and_cursor()
        select_query = f"SELECT * FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(userModel.convert_row_to_user(row))
        
        return users
    
    def get_all_user_id_and_services(self)->list[tuple]:
        """Specifically gets every user's id and corresponding service

        Returns:
            list[tuple]: per tuple, ele 0 is id, ele 1 is website
        """
        connection, cursor = self.get_connection_and_cursor()

        select_query = f"SELECT {constants.USER_TABLE_COL_NAMES[2]}, {constants.USER_TABLE_COL_NAMES[3]} FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        return rows
    
    # various functions
    def know_unknown_post(self, user_id: int, service :str, post_id: int):
        """ Turns a unknown post into known, does not go other way around since input panel handles that

        Args:
            user_id (int): id
            service (str): service
            post_id (int): post id
        """
        user_obj = self.get_user_obj(user_id, service)
        if user_obj is None:
            raise KeyError("User id couldnt find anyone with that id")
        if post_id not in user_obj.unchecked_post_ids:
            raise KeyError("The post id isnt part of unchecked posts")
        if post_id in user_obj.checked_post_ids: # already done
            return
        user_obj.checked_post_ids.append(post_id)
        user_obj.unchecked_post_ids.remove(post_id)
        self.update_database_row_user_object(user_obj)

    def close_all_connections(self):
        """Shuts down all possible connections in known threads
        """
        for connection in connectionList:
            connection.close()