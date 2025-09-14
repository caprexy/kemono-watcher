import sqlite3
import threading
from datetime import date, datetime

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
        try:
            if not getattr(self.thread_data, 'connection', None):
                self.thread_data.connection = sqlite3.connect(urlDatabaseConstants.urlDatabaseName)
            if not getattr(self.thread_data, 'cursor', None):
                self.thread_data.cursor = self.thread_data.connection.cursor()
        except Exception as e:
            print(f"Failed to connect to URL database: {e}")
            raise
    
    def get_connection_n_cursor(self):
        self.connect()
        return getattr(self.thread_data, 'connection', None), \
                getattr(self.thread_data, 'cursor', None)
    
    def createTable(self):
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute(urlDatabaseConstants.userTableCreateCommand)
        connection.commit()

    def addUrl(self, url:str, visited:bool, visited_time:date, service:str, service_id:str, username:str, post_id):
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute('INSERT INTO ' + 
                            urlDatabaseConstants.url_table_name + 
                            f' ({urlDatabaseConstants.url},'+
                            f'{urlDatabaseConstants.visited},'+
                            f'{urlDatabaseConstants.visited_time},' +
                            f'{urlDatabaseConstants.service_id},' +
                            f'{urlDatabaseConstants.service},' +
                            f'{urlDatabaseConstants.post_id},' +
                            f'{urlDatabaseConstants.username})' +
                            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                            [url,visited,visited_time, service_id, service, post_id, username])
        connection.commit()
        
    def deleteUrl(self, unique_id: int):
        # Delete an existing user from the 'users' table based on the
        connection, cursor = self.get_connection_n_cursor()
        try:
            cursor.execute(
                f'DELETE FROM {urlDatabaseConstants.url_table_name} '+
                f'WHERE {urlDatabaseConstants.unique_id} = ?',
                [unique_id]
            )
            connection.commit()
            print(f"User with id {unique_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")
        
    def getAllUrls(self):
        # Retrieve all users from the 'users' table
        connection, cursor = self.get_connection_n_cursor()
        cursor.execute(f'SELECT * FROM {urlDatabaseConstants.url_table_name}')
        res = cursor.fetchall()
        urls = []
        for url in res:
            urls.append(
                self.sqlResRowToUser(url)
            )
        return urls
    

    def getUrlsForUser(self, service: str, service_id: str):
        try:
            connection, cursor = self.get_connection_n_cursor()
            
            query = f"""
            SELECT *
            FROM {urlDatabaseConstants.url_table_name}
            WHERE {urlDatabaseConstants.service} = ? AND {urlDatabaseConstants.service_id} = ?;
            """
            
            cursor.execute(query, (service, service_id))
            res = cursor.fetchall()
            print(f"Database: Found {len(res)} URLs for {service}/{service_id}")
            
            urls = []
            for url_row in res:
                try:
                    url_obj = self.sqlResRowToUser(url_row)
                    urls.append(url_obj)
                except Exception as e:
                    print(f"ERROR processing database row: {e}")
                    continue
                    
            return urls
            
        except Exception as e:
            print(f"ERROR in getUrlsForUser: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
    
    def getAllNotVisitedUrls(self):
        connection, cursor = self.get_connection_n_cursor()
        query = f"""
        SELECT *
        FROM {urlDatabaseConstants.url_table_name}
        WHERE {urlDatabaseConstants.visited} = ?;
        """
        cursor.execute(query, (False,))
        res = cursor.fetchall()
        urls = []
        for url in res:
            urls.append(
                self.sqlResRowToUser(url)
            )
        return urls
    
    def flipUrl(self, url:Url):
        connection, cursor = self.get_connection_n_cursor()
        update_query = f"""
        UPDATE {urlDatabaseConstants.url_table_name}
        SET {urlDatabaseConstants.visited} = ?
        WHERE {urlDatabaseConstants.unique_id} = ?;
        """
        cursor.execute(update_query, (not url.visited, url.unique_id))
        connection.commit()
        
    def sqlResRowToUser(self, url:list):
        try:
            # Database columns: uniqueId, url, postId, visited, visitedTime, service, serviceId, username
            # Url constructor: username, service, service_id, post_id, url, visited, visited_time, unique_id
            result = Url(
                username=url[7],      # username
                service=url[5],       # service  
                service_id=url[6],    # service_id
                post_id=url[2],       # post_id
                url=url[1],           # url
                visited=url[3],       # visited
                visited_time=url[4],  # visited_time
                unique_id=url[0],     # unique_id
            )
            return result
        except Exception as e:
            print(f"ERROR in sqlResRowToUser: {e}")
            print(f"Row data: {url}")
            print(f"Row length: {len(url)}")
            for i, val in enumerate(url):
                print(f"  [{i}]: {val} (type: {type(val)})")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
        
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
    
def postUrlDecrypter(url):
    parts = url.split("/")
    
    if len(parts) == 8 and parts[2] == "kemono.cr" and parts[4] == "user":
        service = parts[3]
        service_id = parts[5]
        post_id = parts[7]
        return service, service_id, post_id
    else:
        # Return None or raise an exception for invalid URLs
        return None