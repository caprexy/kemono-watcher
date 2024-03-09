from controller.database.userDatabaseController import DatabaseController

from view.warningPopup import WarningPopup

class AddUserController():
    
    def __init__(self) -> None:
        self.database_controller = DatabaseController()
    
    def addUser(self,
                username:str,
                service:str,
                service_id:int):
        
        if self.database_controller.does_service_id_exist(service, service_id):
            WarningPopup("This user already exists")
        else:
            self.database_controller.add_user(
                username,
                service,
                service_id
            )