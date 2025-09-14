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
        try:
            if not self.connection:
                self.connection = sqlite3.connect(userDatabaseConstants.userDatabaseName)
            if not self.cursor:
                self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Failed to connect to user database: {e}")
            raise

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
        # Retrieve all users from the 'users' table with unvisited URL counts
        self.connect()
        
        # First, get users with simple query (always works with existing databases)
        self.cursor.execute(f'SELECT * FROM {userDatabaseConstants.user_table_name}')
        user_res = self.cursor.fetchall()
        
        users = []
        for user_row in user_res:
            # Try to get unvisited count for this user
            unvisited_count = 0
            try:
                # Import URL database constants for the count query
                from controller.database import urlDatabaseConstants
                
                # Use URL database controller to get the count (it has the right connection)
                from controller.database.urlDatabaseController import UrlDatabaseController
                url_db_controller = UrlDatabaseController()
                
                # Get connection to URL database
                url_connection, url_cursor = url_db_controller.get_connection_n_cursor()
                
                # Check if URL table exists in the URL database
                url_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (urlDatabaseConstants.url_table_name,))
                table_exists = url_cursor.fetchone()
                
                if table_exists:
                    # Count unvisited URLs for this specific user using URL database connection
                    count_query = f"""
                    SELECT COUNT(*) FROM {urlDatabaseConstants.url_table_name} 
                    WHERE {urlDatabaseConstants.service} = ? 
                    AND {urlDatabaseConstants.service_id} = ? 
                    AND ({urlDatabaseConstants.visited} = 0 OR {urlDatabaseConstants.visited} = 'false' OR {urlDatabaseConstants.visited} = 'False')
                    """
                    
                    service = user_row[2]
                    service_id = str(user_row[3])
                    
                    url_cursor.execute(count_query, (service, service_id))
                    count_result = url_cursor.fetchone()
                    unvisited_count = count_result[0] if count_result else 0
                    
            except Exception:
                # If URL counting fails, just use 0 (backward compatibility)
                unvisited_count = 0
            
            # Create user object with count
            user_obj = User(
                id=user_row[0],
                username=user_row[1],
                service=user_row[2],
                service_id=user_row[3],
                unvisited_count=unvisited_count
            )
            users.append(user_obj)
        
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