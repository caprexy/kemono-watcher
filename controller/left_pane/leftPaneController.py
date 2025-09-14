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
        print("=== showSelectUsersUrls called ===")
        try:
            if self.user_list.selectedRanges() == []: 
                # If no selection, try to get the current row from double-click
                current_row = self.user_list.currentRow()
                print(f"No selection, current row: {current_row}")
                if current_row < 0:
                    print("No valid current row, returning")
                    return []
                selected_rows = [current_row]
            else:
                selected_range = self.user_list.selectedRanges()[0]
                selected_rows = range(selected_range.topRow(), selected_range.bottomRow()+1)
                print(f"Selected range: {selected_range.topRow()} to {selected_range.bottomRow()}")
            
            print(f"Selected rows: {list(selected_rows)}")
            
            # For single user selection, use the filter method to maintain state
            if len(selected_rows) == 1:
                row = selected_rows[0]
                print(f"Processing single user at row {row}")
                
                try:
                    service_item = self.user_list.item(row, userValueIndexes.Service.value)
                    service_id_item = self.user_list.item(row, userValueIndexes.Service_id.value)
                    
                    print(f"Service item: {service_item}")
                    print(f"Service ID item: {service_id_item}")
                    
                    if service_item is None or service_id_item is None:
                        print("ERROR: Service or Service ID item is None")
                        return
                    
                    service = service_item.text()
                    service_id = service_id_item.text()
                    
                    print(f"Service: '{service}', Service ID: '{service_id}'")
                    print(f"Service type: {type(service)}, Service ID type: {type(service_id)}")
                    
                except Exception as e:
                    print(f"ERROR getting service/service_id: {e}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
                    return
                
                try:
                    if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                        print("Using right_pane_controller.setFilterUserSpecific")
                        self.right_pane_controller.setFilterUserSpecific(service, service_id)
                    elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                        print("Using right_pane_url_list.update")
                        urls = self.url_database_controller.getUrlsForUser(service, service_id)
                        print(f"Got {len(urls)} URLs from database")
                        self.right_pane_url_list.update(urls)
                    else:
                        print("ERROR: No right pane controller or URL list available")
                        
                except Exception as e:
                    print(f"ERROR in right pane update: {e}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
                    raise
                    
            else:
                print(f"Processing multiple users: {len(selected_rows)} rows")
                # For multiple users, combine URLs and use direct update
                urls = []
                for row in selected_rows:
                    try:
                        service = self.user_list.item(row, userValueIndexes.Service.value).text()
                        service_id = self.user_list.item(row, userValueIndexes.Service_id.value).text()
                        print(f"Row {row}: service='{service}', service_id='{service_id}'")
                        urls += self.url_database_controller.getUrlsForUser(service, service_id)
                    except Exception as e:
                        print(f"ERROR processing row {row}: {e}")
                        continue
                
                if hasattr(self, 'right_pane_controller') and self.right_pane_controller:
                    # Clear filter state for multi-user selection
                    self.right_pane_controller.current_filter_type = None
                    self.right_pane_controller.current_filter_params = None
                    self.right_pane_controller.url_list_widget.update(urls)
                elif hasattr(self, 'right_pane_url_list') and self.right_pane_url_list:
                    self.right_pane_url_list.update(urls)
                    
            print("=== showSelectUsersUrls completed successfully ===")
            
        except Exception as e:
            print(f"=== ERROR in showSelectUsersUrls: {e} ===")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
        
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