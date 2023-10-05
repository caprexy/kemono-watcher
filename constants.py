"Constants used to define static information from kemono's api and database information"

SERVICES = [
    "Patreon",
    "Fanbox",
    "Discord",
    "Fantia",
    "Afdian",
    "Boosty",
    "DLsite",
    "Gumroad",
    "SubscribeStar",
]

DATABASE_FILENAME = "database.db"

USERS_TABLE_NAME = "user_table"

USER_TABLE_QUERY = f"""
    CREATE TABLE {USERS_TABLE_NAME} (
        program_unique_id INTEGER PRIMARY KEY,
        name TEXT,
        id INTEGER,
        service TEXT,
        known_post_ids TEXT,
        unknown_post_ids TEXT
    )
    """

USER_TABLE_COL_NAMES =[
    "program_unique_id", "name", "id", "service", "known_post_ids", "unknown_post_ids"
]
