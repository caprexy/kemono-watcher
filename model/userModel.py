from enum import Enum

class User:
    def __init__(self,
                id:int,
                username:str,
                service:str,
                service_id:str,
                unvisited_count:int = 0) -> None:
        self.id = id
        self.username = username
        self.service = service
        self.service_id = service_id
        self.unvisited_count = unvisited_count
        
    def values_to_display(self):
        return [self.id, self.username, self.unvisited_count, self.service, self.service_id]
    
    def __str__(self):
        return f'User {self.id} aka {self.username} from {self.service} as user {self.service_id}'
    

def values_names_to_display():
    return [member.name.replace('_', ' ') for member in urlValueIndexes]

class urlValueIndexes(Enum):
    Unique_id = 0
    Username = 1
    Unvisited_count = 2
    Service = 3
    Service_id = 4