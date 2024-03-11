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
    
    def addUrl(self):
        add_url_dialogue = AddUrlDialogue()
        add_url_dialogue.exec()
        self.updateUrlList()
    
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
        self.url_list_widget.update()
    
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
        self.url_list_widget.update()
        
    def updateUrlList(self):
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