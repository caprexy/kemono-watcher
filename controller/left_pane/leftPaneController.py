from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton

from view.left_pane.dialogue.addUserDialogueView import AddUserDialogue
from view.left_pane.dialogue.editUserDialogueView import EditUserDialogue
from view.left_pane.dialogue.deleteUserDialogueView import DeleteUserDialogue
from view.left_pane.components.userListView import UserList
from view.warningPopup import WarningPopup

from controller.database.userDatabaseController import DatabaseController

class LeftPaneController():
    def __init__(self, 
                user_list: UserList) -> None:
        self.database_controller = DatabaseController()
        
        self.user_list = user_list
        
    def openAddUser(self):
        add_user_dialogue = AddUserDialogue(self.updateUserList)
        add_user_dialogue.exec()
        
    def openEditUser(self):
        row_items = self.getOneSelectedUser()
        if row_items is []: return
        
        EditUserDialogue(
            row_items[0],
            row_items[1],
            row_items[2],
            row_items[3],
            self.updateUserList).exec()
        
    def openDeleteUser(self):
        row_items = self.getOneSelectedUser()
        if row_items is []: return
        
        add_user_dialogue = DeleteUserDialogue(
            row_items[0],
            row_items[1],
            row_items[2],
            row_items[3],
            self.updateUserList)
        add_user_dialogue.exec()
        
    def updateUserList(self):
        users = self.database_controller.get_all_users()
        self.user_list.update(users)
    
    def getOneSelectedUser(self):
        if self.user_list.selectedRanges() == []: return []
        
        selected_range = self.user_list.selectedRanges()[0]
        if selected_range.bottomRow() != selected_range.topRow():
            WarningPopup("Select only one row/user please")
            return
        selected_row = selected_range.topRow()
        
        row_items = [self.user_list.item(selected_row, col).text() for col in range(self.user_list.columnCount())]
        return row_items