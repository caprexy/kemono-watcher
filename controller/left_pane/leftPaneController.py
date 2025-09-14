from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton

from view.left_pane.dialogue.addUserDialogueView import AddUserDialogue
from view.left_pane.dialogue.editUserDialogueView import EditUserDialogue
from view.left_pane.dialogue.deleteUserDialogueView import DeleteUserDialogue
from view.left_pane.components.userListView import UserList
from view.right_pane.components.UrlListView import UrlListView
from view.popups import WarningPopup

from controller.database.userDatabaseController import UserDatabaseController
from controller.database.urlDatabaseController import UrlDatabaseController
from controller.left_pane.getUrlsController import UrlsManager

from model.userModel import User
from model.userModel import urlValueIndexes as userValueIndexes
from model.urlModel import urlValueIndexes as urlValueIndexes

class LeftPaneController():
    def __init__(self, 
                user_list: UserList) -> None:
        self.user_database_controller = UserDatabaseController()
        self.url_database_controller = UrlDatabaseController()
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
        
    def getUsersUrl(self, full_url_check_box):
        selected_user = self.getOneSelectedUser()
        if not selected_user: return
        if hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
            self.url_manager.downloadUrls(selected_user, self.right_pane_url_list, full_url_check_box.isChecked())
            self.right_pane_url_list.update()
    
    def getAllUsersUrl(self, full_url_check_box):
        if hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
            self.url_manager.downloadAllUserUrls(self.user_database_controller.getAllUsers(), self.right_pane_url_list, full_url_check_box.isChecked())
            self.right_pane_url_list.update()
        
    def showSelectUsersUrls(self):
        if self.user_list.selectedRanges() == []: 
            # If no selection, try to get the current row from double-click
            current_row = self.user_list.currentRow()
            if current_row < 0:
                return []
            selected_rows = [current_row]
        else:
            selected_range = self.user_list.selectedRanges()[0]
            selected_rows = range(selected_range.topRow(), selected_range.bottomRow()+1)
        
        # For single user selection, use the filter method to maintain state
        if len(selected_rows) == 1:
            row = selected_rows[0]
            service = self.user_list.item(row, userValueIndexes.Service.value).text()
            service_id = self.user_list.item(row, userValueIndexes.Service_id.value).text()
            
            if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                self.right_pane_controller.setFilterUserSpecific(service, service_id)
            elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                urls = self.url_database_controller.getUrlsForUser(service, service_id)
                self.right_pane_url_list.update(urls)
        else:
            # For multiple users, combine URLs and use direct update
            urls = []
            for row in selected_rows:
                service = self.user_list.item(row, userValueIndexes.Service.value).text()
                service_id = self.user_list.item(row, userValueIndexes.Service_id.value).text()
                urls += self.url_database_controller.getUrlsForUser(service, service_id)
            
            if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                # Clear filter state for multi-user selection
                self.right_pane_controller.current_filter_type = None
                self.right_pane_controller.current_filter_params = None
                self.right_pane_controller.url_list_widget.update(urls)
            elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                self.right_pane_url_list.update(urls)
        
    def showAllUsersUrls(self):
        if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
            self.right_pane_controller.setFilterAll()
        elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
            self.right_pane_url_list.update()
    
    def showNotVisitedUrls(self):
        if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
            self.right_pane_controller.setFilterNotVisited()
        else:
            urls = self.url_database_controller.getAllNotVisitedUrls()
            if hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                self.right_pane_url_list.update(urls)
    
    def showNotVisitedUrlsForSelectedUsers(self):
        """Show not visited URLs for the currently selected user(s)."""
        if self.user_list.selectedRanges() == []: 
            # If no selection, try to get the current row from right-click
            current_row = self.user_list.currentRow()
            if current_row < 0:
                return
            selected_rows = [current_row]
        else:
            selected_range = self.user_list.selectedRanges()[0]
            selected_rows = range(selected_range.topRow(), selected_range.bottomRow()+1)
        
        # For single user selection, use the filter method to maintain state
        if len(selected_rows) == 1:
            row = selected_rows[0]
            service = self.user_list.item(row, userValueIndexes.Service.value).text()
            service_id = self.user_list.item(row, userValueIndexes.Service_id.value).text()
            
            if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                self.right_pane_controller.setFilterNotVisitedUserSpecific(service, service_id)
            else:
                # Fallback to direct update
                user_urls = self.url_database_controller.getUrlsForUser(service, service_id)
                unvisited_urls = [url for url in user_urls if not url.visited]
                if hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                    self.right_pane_url_list.update(unvisited_urls)
        else:
            # For multiple users, combine URLs and use direct update
            urls = []
            for row in selected_rows:
                service = self.user_list.item(row, userValueIndexes.Service.value).text()
                service_id = self.user_list.item(row, userValueIndexes.Service_id.value).text()
                user_urls = self.url_database_controller.getUrlsForUser(service, service_id)
                unvisited_urls = [url for url in user_urls if not url.visited]
                urls += unvisited_urls
            
            if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                # Clear filter state for multi-user selection
                self.right_pane_controller.current_filter_type = None
                self.right_pane_controller.current_filter_params = None
                self.right_pane_controller.url_list_widget.update(urls)
            elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                self.right_pane_url_list.update(urls)
        
        
    def updateUserList(self):
        users = self.user_database_controller.getAllUsers()
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
            row_items[userValueIndexes.Unique_id.value],
            row_items[userValueIndexes.Username.value],
            row_items[userValueIndexes.Service.value],
            row_items[userValueIndexes.Service_id.value],
        )
        return selected_user