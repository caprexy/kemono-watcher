from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton

from view.left_pane.dialogue.addUserDialogueView import AddUserDialogue
from view.left_pane.dialogue.editUserDialogueView import EditUserDialogue
from view.left_pane.dialogue.deleteUserDialogueView import DeleteUserDialogue
from view.left_pane.components.userListView import UserList
from view.right_pane.components.UrlListView import UrlListView
from view.warningPopup import WarningPopup

from controller.database.userDatabaseController import UserDatabaseController
from controller.left_pane.getUrlsController import UrlsManager

from model.userModel import User

class LeftPaneController():
    def __init__(self, 
                user_list: UserList) -> None:
        self.database_controller = UserDatabaseController()
        self.url_manager = UrlsManager()
        self.right_pane_url_list = UrlListView()
        self.user_list = user_list
        
    def openAddUser(self):
        add_user_dialogue = AddUserDialogue()
        add_user_dialogue.exec()
        self.updateUserList()
        
    def openEditUser(self):
        selected_user = self.getOneSelectedUser()
        if not selected_user: return
        
        EditUserDialogue(
            selected_user).exec()
        self.updateUserList()
        
    def openDeleteUser(self):
        selected_user = self.getOneSelectedUser()
        if not selected_user: return
        
        add_user_dialogue = DeleteUserDialogue(
            selected_user)
        add_user_dialogue.exec()
        self.updateUserList()
        
    def getUsersUrl(self):
        selected_user = self.getOneSelectedUser()
        if not selected_user: return
        
        self.url_manager.downloadUrls(selected_user, self.right_pane_url_list)
        self.right_pane_url_list.update()
    
    def getAllUsersUrl(self):
        self.url_manager.downloadAllUserUrls(self.database_controller.getAllUsers(), self.right_pane_url_list)
        self.right_pane_url_list.update()
        
    def updateUserList(self):
        users = self.database_controller.getAllUsers()
        self.user_list.update(users)
    
    def getOneSelectedUser(self):
        if self.user_list.selectedRanges() == []: return []
        
        selected_range = self.user_list.selectedRanges()[0]
        if selected_range.bottomRow() != selected_range.topRow():
            WarningPopup("Select only one row/user please")
            return
        selected_row = selected_range.topRow()
        
        row_items = [self.user_list.item(selected_row, col).text() for col in range(self.user_list.columnCount())]
        
        if len(row_items) == 0 :
            return None
        
        selected_user = User(
            row_items[0],
            row_items[1],
            row_items[2],
            row_items[3],
        )
        return selected_user