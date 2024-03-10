import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox

from controller.left_pane.dialogue.addUserController import AddUserController

from view.warningPopup import WarningPopup
import view.left_pane.constants as constants

class AddUrlDialogue(QDialog):
    def __init__(self, update_funct):
        super().__init__()
        
        self.update_funct = update_funct
        
        self.add_url_controller = AddUserController()
        vbox = QVBoxLayout()

        # Create widgets
        urlname_label = QLabel('Username:')
        urlname_input = QLineEdit(self)
        self.urlname_input = urlname_input
        vbox.addWidget(urlname_label)
        vbox.addWidget(urlname_input)

        service_label = QLabel('Service:')
        service_dropdown = QComboBox(self)
        self.service_dropdown = service_dropdown
        [service_dropdown.addItem(service) for service in constants.serviceList]
        vbox.addWidget(service_label)
        vbox.addWidget(service_dropdown)

        service_id_label = QLabel('Url ID:')
        service_id_input = QLineEdit(self)
        self.service_id_input = service_id_input
        vbox.addWidget(service_id_label)
        vbox.addWidget(service_id_input)

        accept_button = QPushButton('Accept', self)
        accept_button.clicked.connect(self.acceptClicked)
        close_button = QPushButton('Close', self)
        close_button.clicked.connect(self.closeWindow)
        vbox.addWidget(accept_button)
        vbox.addWidget(close_button)

        # Set layout for the main window
        self.setLayout(vbox)

        # Set window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Url Input Dialog')
        
    def acceptClicked(self):
        urlname = self.urlname_input.text().strip()
        if urlname == "":
            WarningPopup("Nothing entered for urlname")
            return
        
        service = self.service_dropdown.currentText()
        
        service_id = self.service_id_input.text()
        if service_id == "":
            WarningPopup("Id not entered")
            return
        if not service_id.isdigit():
            WarningPopup("Id is not number")
            return
        
        self.add_url_controller.addUser(urlname, service, service_id)
        self.closeWindow()

    
    def closeWindow(self):
        self.update_funct()
        self.close()