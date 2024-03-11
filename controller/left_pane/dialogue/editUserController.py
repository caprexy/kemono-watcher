from controller.database.userDatabaseController import UserDatabaseController

from view.popups import WarningPopup

class EditUserController():
    
    def __init__(self) -> None:
        self.database_controller = UserDatabaseController()
    
    def editUser(self,
                unique_user_id:int,
                username:str,
                service:str,
                service_id:int):
    
        self.database_controller.editUser(
            unique_user_id,
            username,
            service,
            service_id
        )