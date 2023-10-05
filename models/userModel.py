"""Stores data about a user, all their posts and such"""
import json
from typing import List

class User(object):
    """A user object has some basic information about itself and it's database id
    """
    def __init__(self, 
            database_id: int, 
            name: str, 
            id: int, 
            service: str, 
            checked_post_ids: List[int]=None, 
            unchecked_post_ids: List[int]=None
            ):
        self.database_id = database_id
        self.name = name
        self.id = id
        self.service = service
        self.checked_post_ids = checked_post_ids
        self.unchecked_post_ids = unchecked_post_ids

    def __str__(self):
        return f"User {self.id} of service {self.service}"
    
    def __repr__(self):
        return f"User {self.id} of service {self.service}"

    def get_as_row_tuple(self)->  tuple:
        """Formats a user as a tuple to be used for easy import to database
        Returns:
            tuple: is a tuple of the user's info, note post ids become a string
        """
        return (self.database_id, 
                      self.name, 
                      self.id, 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))

def convert_row_to_user(rowTuple:tuple)-> User:
    """Converts a database row into a user object

    Args:
        rowTuple (_type_): Tuple from the database

    Returns:
        _User: user object built from the tuple
    """
    database_id = rowTuple[0]
    name = rowTuple[1]
    id = rowTuple[2]
    service = rowTuple[3]
    checked_post_ids = json.loads(rowTuple[4])
    unchecked_post_ids = json.loads(rowTuple[5])
    return User(database_id, name, id, service, checked_post_ids, unchecked_post_ids)