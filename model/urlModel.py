from datetime import date
from enum import Enum

visited_text = "visited"
not_visited_text = "not visited"

class Url:
    def __init__(self,
                username:str,
                service:str,
                service_id:str,
                post_id,  # Can be int or str (e.g., 'p-34234')
                url:str,
                visited:bool,
                visited_time:date,
                unique_id:int,
                ) -> None:
        self.url = url
        self.visited = visited
        self.visited_time = visited_time
        self.service = service
        self.service_id = service_id
        self.username = username
        self.post_id = post_id
        self.unique_id = unique_id
        
    def values_to_display(self):
        return [self.username, self.service, self.service_id, self.post_id, self.url, "visited" if self.visited else "not visited", self.visited_time, self.unique_id]
    
    def __str__(self):
        return f'Url {self.post_id} aka {self.url} was {visited_text if self.visited else not_visited_text} at {self.visited_time}'
    
def values_names_to_display():
    return [member.name.replace('_', ' ') for member in urlValueIndexes]

class urlValueIndexes(Enum):
    Username = 0
    Service = 1
    Service_id = 2
    Post_id = 3
    Url = 4
    Visited = 5
    Visited_time = 6
    unique_id = 7