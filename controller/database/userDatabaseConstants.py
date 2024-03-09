userDatabaseName = "userDatabase.db"

userTableName = "users"
userUUIDName = "id"
userUsername = "username"
user_service = "service"
user_service_id = "serviceId"

userTableCreateCommand = f'''
            CREATE TABLE IF NOT EXISTS {userTableName} (
                {userUUIDName} INTEGER PRIMARY KEY,
                {userUsername} TEXT NOT NULL,
                {user_service} TEXT NOT NULL,
                {user_service_id} INTEGER NOT NULL
            )
        '''