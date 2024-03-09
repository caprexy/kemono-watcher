import sqlite3

from controller.database import userDatabaseConstants

from model.user import User

class DatabaseController:
    
    # Ensure is singleton
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseController, cls).__new__(cls)
        return cls._instance
    
    connection = None
    cursor = None
    def __init__(self):
        self.connect()
        self.create_table()
    
    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(userDatabaseConstants.userDatabaseName)
        if not self.cursor:
            self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a 'users' table if it doesn't exist
        self.connect()
        self.cursor.execute(userDatabaseConstants.userTableCreateCommand)
        self.connection.commit()

    def add_user(self, username:str, user_service:str, user_service_id:int):
        # Insert a new user into the 'users' table
        self.connect()
        self.cursor.execute('INSERT INTO ' + 
                            userDatabaseConstants.userTableName + 
                            f' ({userDatabaseConstants.userUsername},'+
                            f'{userDatabaseConstants.user_service},'+
                            f'{userDatabaseConstants.user_service_id})' +
                            ' VALUES (?, ?, ?)',
                            [username,user_service,user_service_id])
        self.connection.commit()
        
    def edit_user(self, unique_id: int, username: str, user_service: str, user_service_id: int):
        # Update an existing user in the 'users' table based on the 
        self.connect()
        try:
            self.cursor.execute(
                f'UPDATE {userDatabaseConstants.userTableName} '+
                f'SET {userDatabaseConstants.userUsername} = ?, '+
                f'{userDatabaseConstants.user_service} = ?, '+
                f'{userDatabaseConstants.user_service_id} = ? '+
                f'WHERE {userDatabaseConstants.userUUIDName} = ?',
                [username, user_service, user_service_id, unique_id]
            )
            self.connection.commit()
            print(f"User with id {unique_id} updated successfully.")
        except Exception as e:
            print(f"Error updating user: {e}")
            
    def delete_user(self, unique_id: int):
        # Delete an existing user from the 'users' table based on the
        self.connect()
        try:
            self.cursor.execute(
                f'DELETE FROM {userDatabaseConstants.userTableName} '+
                f'WHERE {userDatabaseConstants.userUUIDName} = ?',
                [unique_id]
            )
            self.connection.commit()
            print(f"User with id {unique_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")


        
    def get_all_users(self):
        # Retrieve all users from the 'users' table
        self.connect()
        self.cursor.execute(f'SELECT * FROM {userDatabaseConstants.userTableName}')
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
    
    def does_service_id_exist(self, service:str, service_id:int):
        query = f"""
        SELECT COUNT(*) AS count
        FROM {userDatabaseConstants.userTableName}
        WHERE {userDatabaseConstants.user_service} = ? AND {userDatabaseConstants.user_service_id} = ?;
        """
        self.cursor.execute(query, (service, service_id))
        result = self.cursor.fetchone()
        return result[0] == 1