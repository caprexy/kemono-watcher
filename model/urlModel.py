from datetime import date

class Url:
    def __init__(self,
                unique_id:int,
                url:str,
                visited:bool,
                visited_time:date,
                service:str,
                service_id:str,
                username:str
                ) -> None:
        self.id = unique_id
        self.url = url
        self.visited = visited
        self.visited_time = visited_time
        self.service = service
        self.service_id = service_id
        self.username = username
        
    def values_to_display(self):
        return [self.username, self.service, self.service_id, self.url, self.visited, self.visited_time]
    
    def __str__(self):
        return f'Url {self.id} aka {self.url} was {"visited" if self.visited else "not visited"} at {self.visited_time}'
    

def values_names_to_display():
    return ["Username", "Service", "Service Id", "Url", "Visited", "Visited time"]