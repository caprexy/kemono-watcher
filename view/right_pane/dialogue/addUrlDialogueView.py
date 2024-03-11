import sys
from PyQt6.QtWidgets import QCheckBox, QDialog, QLabel, QLineEdit, QPushButton, QDateTimeEdit, QVBoxLayout, QComboBox

from controller.right_pane.dialogue.addUrlController import AddUrlController
from controller.left_pane.kemonoApiController import postUrlDecrypter

from view.popups import WarningPopup
import view.left_pane.constants as constants

from model.urlModel import urlValueIndexes

class AddUrlDialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.add_url_controller = AddUrlController()
        vbox = QVBoxLayout()
        
        username_label = QLabel(urlValueIndexes.Username.name +':')
        username_input = QLineEdit(self)
        self.username_input = username_input
        vbox.addWidget(username_label)
        vbox.addWidget(username_input)
        
        url_label = QLabel(urlValueIndexes.Url.name +':')
        url_input = QLineEdit(self)
        self.url_input = url_input
        vbox.addWidget(url_label)
        vbox.addWidget(url_input)
        
        visited_label = QLabel(urlValueIndexes.Visited.name.replace("_"," ") +':')
        visited_checkbox = QCheckBox(self)
        visited_checkbox.setChecked(True)
        self.visited_checkbox = visited_checkbox
        vbox.addWidget(visited_label)
        vbox.addWidget(visited_checkbox)

        accept_button = QPushButton('Accept', self)
        accept_button.clicked.connect(self.acceptClicked)
        close_button = QPushButton('Close', self)
        close_button.clicked.connect(self.close)
        vbox.addWidget(accept_button)
        vbox.addWidget(close_button)

        # Set layout for the main window
        self.setLayout(vbox)

        # Set window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Url Input Dialog')
        
    def acceptClicked(self):
        username = self.username_input.text().strip()
        if username == "":
            WarningPopup("Nothing entered for username")
            return
        
        url = self.url_input.text().strip()
        if url == "":
            WarningPopup("Nothing entered for url")
            return
        
        visited = self.visited_checkbox.isChecked()
        
        if postUrlDecrypter(url) is None:
            WarningPopup("Couldnt decrypt url")
            return
        service, service_id, post_id = postUrlDecrypter(url)
        
        self.add_url_controller.addUrl(
            username=username, 
            post_id=post_id, 
            url=url,
            service=service, 
            service_id=service_id, 
            visited=visited)
        self.closeWindow()