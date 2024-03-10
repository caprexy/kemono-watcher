from controller.database.userDatabaseController import UserDatabaseController

class DeleteUserController():
    
    def __init__(self) -> None:
        self.database_controller = UserDatabaseController()
    
    def deleteUser(self,
                unique_user_id:int):
        self.database_controller.deleteUser(
            unique_user_id
        )