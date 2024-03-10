import sqlite3
import threading
from datetime import date

from controller.database import urlDatabaseConstants

from model.urlModel import Url

class UrlDatabaseController:
    
    # Ensure is singleton
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UrlDatabaseController, cls).__new__(cls)
        return cls._instance
    
    thread_data = threading.local()
    thread_data.connection = None
    thread_data.cursor = None
    
    def __init__(self):
        self.connect()
        self.createTable()
    
    def connect(self):
        if not getattr(self.thread_data, 'connection', None):
            self.thread_data.connection = sqlite3.connect(urlDatabaseConstants.urlDatabaseName)
        if not getattr(self.thread_data, 'cursor', None):
            self.thread_data.cursor = self.thread_data.connection.cursor()
    
    def get_connection_n_cursor(self):
        self.connect()
        return getattr(self.thread_data, 'connection', None), \
                getattr(self.thread_data, 'cursor', None)
    
    def createTable(self):
        # Create a 'users' table if it doesn't exist
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute(urlDatabaseConstants.userTableCreateCommand)
        connection.commit()

    def addUrl(self, url:str, visited:bool, visited_time:date, service:str, service_id:str, username:str):
        # Insert a new user into the 'users' table
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute('INSERT INTO ' + 
                            urlDatabaseConstants.url_table_name + 
                            f' ({urlDatabaseConstants.url},'+
                            f'{urlDatabaseConstants.visited},'+
                            f'{urlDatabaseConstants.visited_time},' +
                            f'{urlDatabaseConstants.service_id},' +
                            f'{urlDatabaseConstants.service},' +
                            f'{urlDatabaseConstants.username})' +
                            ' VALUES (?, ?, ?, ?, ?, ?)',
                            [url,visited,visited_time, service_id, service, username])
        connection.commit()
        
    # def editUser(self, unique_id: int, username: str, user_service: str, user_service_id: int):
    #     # Update an existing user in the 'users' table based on the 
    #     self.connect()
    #     try:
    #         self.cursor.execute(
    #             f'UPDATE {urlDatabaseConstants.user_table_name} '+
    #             f'SET {urlDatabaseConstants.user_username} = ?, '+
    #             f'{urlDatabaseConstants.user_service} = ?, '+
    #             f'{urlDatabaseConstants.user_service_id} = ? '+
    #             f'WHERE {urlDatabaseConstants.user_unique_id} = ?',
    #             [username, user_service, user_service_id, unique_id]
    #         )
    #         self.connection.commit()
    #         print(f"User with id {unique_id} updated successfully.")
    #     except Exception as e:
    #         print(f"Error updating user: {e}")
            
    # def deleteUser(self, unique_id: int):
    #     # Delete an existing user from the 'users' table based on the
    #     self.connect()
    #     try:
    #         self.cursor.execute(
    #             f'DELETE FROM {urlDatabaseConstants.user_table_name} '+
    #             f'WHERE {urlDatabaseConstants.user_unique_id} = ?',
    #             [unique_id]
    #         )
    #         self.connection.commit()
    #         print(f"User with id {unique_id} deleted successfully.")
    #     except Exception as e:
    #         print(f"Error deleting user: {e}")


        
    def getAllUrls(self):
        # Retrieve all users from the 'users' table
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute(f'SELECT * FROM {urlDatabaseConstants.url_table_name}')
        res = cursor.fetchall()
        urls = []
        for url in res:
            urls.append(
                Url(
                    url[0],
                    url[1],
                    url[2],
                    url[3],
                    url[4],
                    url[5],
                    url[6]
                )
            )
        return urls
    
    def doesUrlExist(self, url:str):
        connection, cursor = self.get_connection_n_cursor()
        query = f"""
        SELECT COUNT(*) AS count
        FROM {urlDatabaseConstants.url_table_name}
        WHERE {urlDatabaseConstants.url} = ?;
        """
        cursor.execute(query, (url,))
        result = cursor.fetchone()
        return result[0] == 1