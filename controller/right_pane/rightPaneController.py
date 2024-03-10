from view.right_pane.components.UrlListView import UrlListView

from view.right_pane.dialogue.addUrlDialogueView import AddUrlDialogue

class RightPaneController():
    def __init__(self, url_list_widget:UrlListView) -> None:
        self.url_list_widget = url_list_widget
    
    def addUrl(self):
        add_url_dialogue = AddUrlDialogue(self.updateUrlList)
        add_url_dialogue.exec()
    
    def editUrl(self):
        pass
    
    def deleteUrl(self):
        pass
    
    def updateUrlList(self):
        pass
    