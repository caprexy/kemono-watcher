userDatabaseName = "userDatabase.db"

user_table_name = "users"
user_unique_id = "id"
user_username = "username"
user_service = "service"
user_service_id = "serviceId"

userTableCreateCommand = f'''
            CREATE TABLE IF NOT EXISTS {user_table_name} (
                {user_unique_id} INTEGER PRIMARY KEY,
                {user_username} TEXT NOT NULL,
                {user_service} TEXT NOT NULL,
                {user_service_id} INTEGER NOT NULL
            )
        '''