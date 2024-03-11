from datetime import datetime

from controller.database.urlDatabaseController import UrlDatabaseController

from view.popups import WarningPopup

class AddUrlController():
    
    def __init__(self) -> None:
        self.database_controller = UrlDatabaseController()
    
    def addUrl(self,
                username:str,
                url:str,
                service:str,
                service_id:int,
                post_id:int,
                visited:bool):
        
        if self.database_controller.doesUrlExist(url):
            WarningPopup("This url already exists")
        else:
            self.database_controller.addUrl(
                url=url,
                visited=visited,
                visited_time=datetime.now().date() if visited else None,
                service=service,
                service_id=service_id,
                username=username,
                post_id=post_id
            )