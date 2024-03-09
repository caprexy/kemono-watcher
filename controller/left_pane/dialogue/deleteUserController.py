from controller.database.userDatabaseController import DatabaseController

class DeleteUserController():
    
    def __init__(self) -> None:
        self.database_controller = DatabaseController()
    
    def deleteUser(self,
                unique_user_id:int):
        self.database_controller.delete_user(
            unique_user_id
        )