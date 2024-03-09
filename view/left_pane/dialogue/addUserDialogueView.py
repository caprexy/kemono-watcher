import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox

from controller.left_pane.dialogue.addUserController import AddUserController

from view.warningPopup import WarningPopup
import view.left_pane.constants as constants

class AddUserDialogue(QDialog):
    def __init__(self, update_funct):
        super().__init__()
        
        self.update_funct = update_funct
        
        self.add_user_controller = AddUserController()
        vbox = QVBoxLayout()

        # Create widgets
        username_label = QLabel('Username:')
        username_input = QLineEdit(self)
        self.username_input = username_input
        vbox.addWidget(username_label)
        vbox.addWidget(username_input)

        service_label = QLabel('Service:')
        service_dropdown = QComboBox(self)
        self.service_dropdown = service_dropdown
        [service_dropdown.addItem(service) for service in constants.serviceList]
        vbox.addWidget(service_label)
        vbox.addWidget(service_dropdown)

        service_id_label = QLabel('User ID:')
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
        self.setWindowTitle('User Input Dialog')
        
    def acceptClicked(self):
        username = self.username_input.text().strip()
        if username == "":
            WarningPopup("Nothing entered for username")
            return
        
        service = self.service_dropdown.currentText()
        
        service_id = self.service_id_input.text()
        if service_id == "":
            WarningPopup("Id not entered")
            return
        if not service_id.isdigit():
            WarningPopup("Id is not number")
            return
        
        self.add_user_controller.addUser(username, service, service_id)
        self.closeWindow()

    
    def closeWindow(self):
        self.update_funct()
        self.close()