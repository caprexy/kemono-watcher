from controller.database.userDatabaseController import UserDatabaseController

from view.popups import WarningPopup

class AddUserController():
    
    def __init__(self) -> None:
        self.database_controller = UserDatabaseController()
    
    def addUser(self,
                username:str,
                service:str,
                service_id:int):
        
        if self.database_controller.doesServiceIdExist(service, service_id):
            WarningPopup("This user already exists")
        else:
            self.database_controller.addUser(
                username,
                service,
                service_id
            )