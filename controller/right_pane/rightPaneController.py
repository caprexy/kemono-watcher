from PyQt6.QtWidgets import QMessageBox
import webbrowser

from controller.database.urlDatabaseController import UrlDatabaseController

from view.popups import WarningPopup, ConfirmPopup
from view.right_pane.components.UrlListView import UrlListView
from view.right_pane.dialogue.addUrlDialogueView import AddUrlDialogue

from model.urlModel import Url, visited_text, urlValueIndexes
from model.userModel import urlValueIndexes as userValueIndexes

class RightPaneController():
    def __init__(self, url_list_widget:UrlListView) -> None:
        self.url_list_widget = url_list_widget
        self.url_database_controller = UrlDatabaseController()
        
        # Track current filter state
        self.current_filter_type = None  # 'all', 'user_specific', 'not_visited', 'not_visited_user_specific'
        self.current_filter_params = None  # Store parameters for the current filter
    
    def addUrl(self):
        add_url_dialogue = AddUrlDialogue()
        add_url_dialogue.exec()
        self._refresh_current_filter()
    
    def deleteUrl(self):
        urls = self.getSelectedUrls()
        if urls == []:
            return
        
        confirm_popup = ConfirmPopup("Delete the selected rows")
        confirm_popup_res = confirm_popup.exec()
        
        if confirm_popup_res != QMessageBox.StandardButton.Yes:
            return
        
        for url in urls:
            self.url_database_controller.deleteUrl(url.unique_id)
        self._refresh_current_filter()
    
    def openUrls(self):
        urls = self.getSelectedUrls()
        if urls == []: return
        
        for url in urls:
            webbrowser.open(url.url, autoraise=True)
        
    def flipUrl(self):
        urls = self.getSelectedUrls()
        if urls == []: return
        
        for url in urls:
            self.url_database_controller.flipUrl(url)
        self._refresh_current_filter()
        
    def updateUrlList(self):
        """Update URL list maintaining current filter."""
        self._refresh_current_filter()
    
    def setFilterAll(self):
        """Set filter to show all URLs."""
        self.current_filter_type = 'all'
        self.current_filter_params = None
        self.url_list_widget.update()
    
    def setFilterUserSpecific(self, service, service_id):
        """Set filter to show URLs for specific user."""
        self.current_filter_type = 'user_specific'
        self.current_filter_params = {'service': service, 'service_id': service_id}
        urls = self.url_database_controller.getUrlsForUser(service, service_id)
        self.url_list_widget.update(urls)
    
    def setFilterNotVisited(self):
        """Set filter to show all not visited URLs."""
        self.current_filter_type = 'not_visited'
        self.current_filter_params = None
        urls = self.url_database_controller.getAllNotVisitedUrls()
        self.url_list_widget.update(urls)
    
    def setFilterNotVisitedUserSpecific(self, service, service_id):
        """Set filter to show not visited URLs for specific user."""
        self.current_filter_type = 'not_visited_user_specific'
        self.current_filter_params = {'service': service, 'service_id': service_id}
        user_urls = self.url_database_controller.getUrlsForUser(service, service_id)
        unvisited_urls = [url for url in user_urls if not url.visited]
        self.url_list_widget.update(unvisited_urls)
    
    def showUserUrls(self, service, service_id):
        """Show all URLs for the specified user (triggered by clicking on a URL)."""
        self.setFilterUserSpecific(service, service_id)
    
    def showUserUnvisitedUrls(self, service, service_id):
        """Show unvisited URLs for the specified user (triggered by context menu)."""
        self.setFilterNotVisitedUserSpecific(service, service_id)
    
    def _refresh_current_filter(self):
        """Refresh the current filter to maintain the view after changes."""
        if self.current_filter_type == 'all':
            self.url_list_widget.update()
        elif self.current_filter_type == 'user_specific':
            if self.current_filter_params:
                urls = self.url_database_controller.getUrlsForUser(
                    self.current_filter_params['service'], 
                    self.current_filter_params['service_id']
                )
                self.url_list_widget.update(urls)
        elif self.current_filter_type == 'not_visited':
            urls = self.url_database_controller.getAllNotVisitedUrls()
            self.url_list_widget.update(urls)
        elif self.current_filter_type == 'not_visited_user_specific':
            if self.current_filter_params:
                user_urls = self.url_database_controller.getUrlsForUser(
                    self.current_filter_params['service'], 
                    self.current_filter_params['service_id']
                )
                unvisited_urls = [url for url in user_urls if not url.visited]
                self.url_list_widget.update(unvisited_urls)
        else:
            # Default to all URLs if no filter is set
            self.url_list_widget.update()
    
    def getSelectedUrls(self, one_only=False)->list[Url]:
        selected_items = self.url_list_widget.selectedItems()
        if selected_items == []: return []
        
        selected_urls = []
        spacing = len(list(urlValueIndexes))-1 #theres a hidden column that selectedItems will not catch
        url_count = 0
        for index in range(0, len(selected_items), spacing):
            url_count += 1
            if one_only and url_count > 1:
                WarningPopup("Select only one row/url please")
                return []
            desired_row = selected_items[index].row()
            row_text = [self.url_list_widget.item(desired_row, col).text() for col in range(self.url_list_widget.columnCount())]
            row_text[urlValueIndexes.Visited.value] = True if row_text[urlValueIndexes.Visited.value] == visited_text else False
            selected_urls.append(Url(*row_text))
        return selected_urls