urlDatabaseName = "urlDatabase.db"

url_table_name = "urls"
unique_id = "uniqueId"
url = "url"
visited = "visited"
visited_time = "visitedTime"
service = "service"
service_id = "serviceId"
post_id = "postId"
username = "username"

userTableCreateCommand = f'''
            CREATE TABLE IF NOT EXISTS {url_table_name} (
                {unique_id} INTEGER PRIMARY KEY,
                {url} TEXT NOT NULL,
                {post_id} TEXT NOT NULL, 
                {visited} BOOLEAN NOT NULL,
                {visited_time} DATE,
                {service} TEXT NOT NULL,
                {service_id} TEXT NOT NUll,
                {username} TEXT NOT NULL
            )
        '''