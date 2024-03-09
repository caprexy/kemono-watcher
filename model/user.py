class User:
    def __init__(self,
                id:int,
                username:str,
                service:str,
                service_id:str) -> None:
        self.id = id
        self.username = username
        self.service = service
        self.service_id = service_id
        
    def values_to_display(self):
        return [self.id, self.username, self.service, self.service_id]
    
    def __str__(self):
        return f'User {self.id} aka {self.username} from {self.service} as user {self.service_id}'
    

def values_names_to_display():
    return ["Unique id", "Username", "Service", "Service_id"]