import sqlite3

from controller.database import userDatabaseConstants

from model.userModel import User

class UserDatabaseController:
    
    # Ensure is singleton
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UserDatabaseController, cls).__new__(cls)
        return cls._instance
    
    connection = None
    cursor = None
    def __init__(self):
        self.connect()
        self.createTable()
    
    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(userDatabaseConstants.userDatabaseName)
        if not self.cursor:
            self.cursor = self.connection.cursor()

    def createTable(self):
        # Create a 'users' table if it doesn't exist
        self.connect()
        self.cursor.execute(userDatabaseConstants.userTableCreateCommand)
        self.connection.commit()

    def addUser(self, username:str, user_service:str, user_service_id:int):
        # Insert a new user into the 'users' table
        self.connect()
        self.cursor.execute('INSERT INTO ' + 
                            userDatabaseConstants.user_table_name + 
                            f' ({userDatabaseConstants.user_username},'+
                            f'{userDatabaseConstants.user_service},'+
                            f'{userDatabaseConstants.user_service_id})' +
                            ' VALUES (?, ?, ?)',
                            [username,user_service,user_service_id])
        self.connection.commit()
        
    def editUser(self, unique_id: int, username: str, user_service: str, user_service_id: int):
        # Update an existing user in the 'users' table based on the 
        self.connect()
        try:
            self.cursor.execute(
                f'UPDATE {userDatabaseConstants.user_table_name} '+
                f'SET {userDatabaseConstants.user_username} = ?, '+
                f'{userDatabaseConstants.user_service} = ?, '+
                f'{userDatabaseConstants.user_service_id} = ? '+
                f'WHERE {userDatabaseConstants.user_unique_id} = ?',
                [username, user_service, user_service_id, unique_id]
            )
            self.connection.commit()
            print(f"User with id {unique_id} updated successfully.")
        except Exception as e:
            print(f"Error updating user: {e}")
            
    def deleteUser(self, unique_id: int):
        # Delete an existing user from the 'users' table based on the
        self.connect()
        try:
            self.cursor.execute(
                f'DELETE FROM {userDatabaseConstants.user_table_name} '+
                f'WHERE {userDatabaseConstants.user_unique_id} = ?',
                [unique_id]
            )
            self.connection.commit()
            print(f"User with id {unique_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")

    def getAllUsers(self):
        # Retrieve all users from the 'users' table
        self.connect()
        self.cursor.execute(f'SELECT * FROM {userDatabaseConstants.user_table_name}')
        res = self.cursor.fetchall()
        users = []
        for user in res:
            users.append(
                User(
                    user[0],
                    user[1],
                    user[2],
                    user[3]
                )
            )
        return users
    
    def doesServiceIdExist(self, service:str, service_id:int):
        query = f"""
        SELECT COUNT(*) AS count
        FROM {userDatabaseConstants.user_table_name}
        WHERE {userDatabaseConstants.user_service} = ? AND {userDatabaseConstants.user_service_id} = ?;
        """
        self.cursor.execute(query, (service, service_id))
        result = self.cursor.fetchone()
        return result[0] == 1