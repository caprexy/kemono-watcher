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
    def __init__(self):
        logging.info("Creating new database object")
        # gathering cursors and connections to be closed later on
        self.thread_data = threading.local()

        connection, cursor = self.getConnectionAndCursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{constants.USERS_TABLE_NAME}'")
        existing_table = cursor.fetchone()

        if existing_table is None:
            cursor.execute(constants.USER_TABLE_QUERY)
            logging.info("Creating new table")
        else:
            logging.info("Found table")

    # funcitons to allows each thread to have their own connection
    def getConnectionAndCursor(self): 
        if not hasattr(self.thread_data, "connection") or self.thread_data.connection == None:
            self.thread_data.connection = sqlite3.connect(constants.DATABASE_FILENAME)
            connectionList.append(self.thread_data.connection)
            self.thread_data.cursor = self.thread_data.connection.cursor()
            cursorList.append(self.thread_data.cursor)
        return self.thread_data.connection, self.thread_data.cursor
    
    def closeThreadConnections(self):
        if hasattr(self.thread_data, "cursor"):
            cursorList.remove(self.thread_data.cursor)
            self.thread_data.cursor.close()
            self.thread_data.cursor = None
        if hasattr(self.thread_data, "connection"):
            connectionList.remove(self.thread_data.connection)
            self.thread_data.connection.close()
            self.thread_data.connection = None

    def createUser(self, id: int, service: str, addButton, *staticCallbacks):
        threadConnection, threadCursor = self.getConnectionAndCursor()
        try:
            # get ids
            statusHelper.setuserOperationStatusValues("Got 0 user posts", "orange")

            request = "https://kemono.party/api/" + service.lower() + "/user/" + str(id) + "?o="
            i = 0
            knownIdList = []
            statusHelper.setuserOperationStatusValues("Looking for posts",  "orange")
            contents = urllib.request.urlopen(request + str(i)).read()
            response = json.loads(contents.decode())
            while(bool(response)): #keep running while contents exists
                statusHelper.setuserOperationStatusValues("Got " +str(i)+" user posts and looking more",  "orange")
                for obj in response:
                    knownIdList.append(int(obj["id"]))

                i += 50
                contents = urllib.request.urlopen(request + str(i)).read()
                response = json.loads(contents.decode())

            statusHelper.setuserOperationStatusValues("Finished getting all posts",  "orange")

            # actually write the new user and put it into the database
            knownIdListJson = json.dumps(knownIdList)
            unknownIdListJson = json.dumps([])
            insertQuery = f"INSERT INTO {constants.USERS_TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?)"
            dataToInsert = (None, "na", id, service, knownIdListJson, unknownIdListJson)
            threadCursor.execute(insertQuery, dataToInsert)
            statusHelper.setuserOperationStatusValues("User is now in database, reclick to view",  "green")
            addButton["state"] = "normal"
            threadConnection.commit()
            
            for callback in staticCallbacks:
                callback()

        except Exception as e:
            logging.error("Failed to add a user: "+str(e))
            threadConnection.rollback()
        finally:
            self.closeThreadConnections()
            pass

    # basic crud, basically we can change anything but the database id
    def replaceDatabaseIdRow(self, userObj:userModel.User):
        logging.info("Updating user: "+str(userObj))
        connection, cursor = self.getConnectionAndCursor()
        rowTuple = userObj.getAsRowTuple()
        databaseId = rowTuple[0]

        set_clause = ", ".join(f"{column} = ?" for column in constants.USER_TABLE_COL_NAMES[1:])
        update_query = f"UPDATE {constants.USERS_TABLE_NAME} SET {set_clause} WHERE {constants.USER_TABLE_COL_NAMES[0]} = ?"
        values = rowTuple[1:] + (databaseId,)

        cursor.execute(update_query, values)
        connection.commit()

    def updateUserData(self, userId: int, service: str, knownIds: List[int], unknownIds:List[int]):
        userObj = self.getUserObj(userId,service)
        if userObj == None:
            raise ValueError("Couldnt find a user object")
        userObj.checkedPostIds = knownIds
        userObj.uncheckedPostIds = unknownIds 
        self.replaceDatabaseIdRow(userObj)

    def deleteUser(self, userId: int, service: str, *staticCallbacks):
        connection, cursor = self.getConnectionAndCursor()
        try:    
            delete_query = f"DELETE FROM {constants.USERS_TABLE_NAME} WHERE {constants.USER_TABLE_COL_NAMES[2]} = ? AND {constants.USER_TABLE_COL_NAMES[3]} = ?"
            print(delete_query)
            cursor.execute(delete_query, (userId, service))
            connection.commit()
            statusHelper.setuserOperationStatusValues("Deleted user", "green")

            for callback in staticCallbacks:
                callback()
        except Exception as e:
            logging.error("Failed to delete a user: "+str(e))
            statusHelper.setuserOperationStatusValues("Failed to delete user", "red")
            connection.rollback()
        finally:
            self.closeThreadConnections()
            pass

    # various gets
    def getAllUnknownPostsIdandService(self):
        connection, cursor = self.getConnectionAndCursor()

        select_query = f"SELECT {constants.USER_TABLE_COL_NAMES[5]},{constants.USER_TABLE_COL_NAMES[3]},{constants.USER_TABLE_COL_NAMES[2]} FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        unknownPosts = []
        for row in rows:
            for postId in json.loads(row[0]):
                unknownPosts.append(f"{postId},{row[1]},{row[2]}")

        return unknownPosts
    
    def userExists(self, userId: int, service: str):
        return bool(self.getUserObj(userId, service))
    
    def getUserObj(self, userId: int, service: str):
        connection, cursor = self.getConnectionAndCursor()

        select_query = f"SELECT * FROM {constants.USERS_TABLE_NAME} WHERE id = ? AND website = ?"
        cursor.execute(select_query, (userId, service))

        row = cursor.fetchone()
        if row == None: return None

        return userModel.convertRowIntoUser(row)

    def getAllUsersObj(self):
        connection, cursor = self.getConnectionAndCursor()
        select_query = f"SELECT * FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(userModel.convertRowIntoUser(row))
        
        return users
    
    def getAllUserIdServices(self):
        connection, cursor = self.getConnectionAndCursor()

        select_query = f"SELECT id, website FROM {constants.USERS_TABLE_NAME}"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        return rows
    
    # various functions
    def knowUnknownPost(self, userId: int, service, postId: int):
        userObj = self.getUserObj(userId, service)
        if userObj == None:
            raise KeyError("User id couldnt find anyone with that id")
        if postId not in userObj.uncheckedPostIds:
            raise KeyError("The post id isnt part of unchecked posts")
        if postId in userObj.checkedPostIds: # already done
            return
        userObj.checkedPostIds.append(postId)
        userObj.uncheckedPostIds.remove(postId)
        self.replaceDatabaseIdRow(userObj)

    def closeAllConnections(self):
        for connection in connectionList:
            connection.close()