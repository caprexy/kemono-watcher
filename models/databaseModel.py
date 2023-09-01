import constants
import urllib.request
import json
import logging
import sqlite3
import threading

from . import userModel
from inputPanel import statusHelper

class Database(object):
    def __init__(self):
        logging.info("Creating new database object")
        self.connection_pool = threading.local()
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
        if not hasattr(self.connection_pool, "connection"):
            self.connection_pool.connection = sqlite3.connect(constants.DATABASE_FILENAME)
            self.connection_pool.cursor = self.connection_pool.connection.cursor()
        return self.connection_pool.connection, self.connection_pool.cursor
    
    def close_connection(self):
        if hasattr(self.connection_pool, "connection"):
            self.connection_pool.connection.close()
            self.connection_pool.connection = None
    
    # basic crud
    def updateUserObj(self, userObj):
        logging.info("Updating user: "+str(userObj))
        connection, cursor = self.getConnectionAndCursor()
        rowTuple = userObj.getAsRowTuple()
        databaseId = rowTuple[0]

        set_clause = ", ".join(f"{column} = ?" for column in constants.USER_TABLE_COL_NAMES[1:])
        update_query = f"UPDATE {constants.USERS_TABLE_NAME} SET {set_clause} WHERE {constants.USER_TABLE_COL_NAMES[0]} = ?"
        values = rowTuple[1:] + (databaseId,)

        cursor.execute(update_query, values)
        connection.commit()

    def updateUserData(self, user, service, knownIds, unknownIds):
        userObj = self.getUserObj(user,service)
        userObj.checkedPostIds = knownIds
        userObj.uncheckedPostIds = unknownIds 
        self.updateUserObj(userObj)

    def deleteUser(self, user, service, *staticCallbacks):
        connection, cursor = self.getConnectionAndCursor()
        try:    
            delete_query = f"DELETE FROM {constants.USERS_TABLE_NAME} WHERE {constants.USER_TABLE_COL_NAMES[2]} = ? AND {constants.USER_TABLE_COL_NAMES[3]} = ?"
            print(delete_query)
            cursor.execute(delete_query, (user, service))
            connection.commit()
            statusHelper.setuserOperationStatusValues("Deleted user", "green")

            for callback in staticCallbacks:
                callback()
        except Exception as e:
            logging.error("Failed to delete a user: "+str(e))
            statusHelper.setuserOperationStatusValues("Failed to delete user", "red")
            connection.rollback()
        finally:
            self.close_connection()
            pass

    def createUser(self, id, service, addButton, *staticCallbacks):
        try:
            threadConnection, threadCursor = self.getConnectionAndCursor()

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
                    knownIdList.append(obj["id"])

                i += 50
                contents = urllib.request.urlopen(request + str(i)).read()
                response = json.loads(contents.decode())

            statusHelper.setuserOperationStatusValues("Finished getting all posts",  "orange")

            # actually write the new user and put it into the database
            knownIdListJson = json.dumps(knownIdList)
            unknownIdListJson = json.dumps("")
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
            self.close_connection()
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
    
    def userExists(self, userId, service):
        return bool(self.getUserObj(userId, service))
    
    def getUserObj(self, userId, service):
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
    def knowUnknownPost(self, userId, service, postId):
        userObj = self.getUserObj(userId, service)
        userObj.checkedPostIds.append(postId)
        userObj.uncheckedPostIds.remove(postId)
        self.updateUserObj(userObj)
