from controller.database.userDatabaseController import DatabaseController

from view.warningPopup import WarningPopup

class EditUserController():
    
    def __init__(self) -> None:
        self.database_controller = DatabaseController()
    
    def editUser(self,
                unique_user_id:int,
                username:str,
                service:str,
                service_id:int):
    
        self.database_controller.edit_user(
            unique_user_id,
            username,
            service,
            service_id
        )