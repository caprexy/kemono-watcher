import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox

from controller.left_pane.dialogue.editUserController import EditUserController

from view.popups import WarningPopup
import view.left_pane.constants as constants

from model.userModel import User

class EditUserDialogue(QDialog):
    def __init__(self, 
                user:User,
                ):
        super().__init__()
        
        self.unique_user_id = user.id
        
        self.edit_user_controller = EditUserController()
        vbox = QVBoxLayout()

        username_label = QLabel('Username:')
        username_input = QLineEdit(self)
        username_input.setText(user.username)
        self.username_input = username_input
        vbox.addWidget(username_label)
        vbox.addWidget(username_input)

        service_label = QLabel('Service:')
        service_dropdown = QComboBox(self)
        self.service_dropdown = service_dropdown
        [service_dropdown.addItem(service) for service in constants.serviceList]
        service_dropdown.setCurrentText(user.service)
        vbox.addWidget(service_label)
        vbox.addWidget(service_dropdown)

        service_id_label = QLabel('User ID:')
        service_id_input = QLineEdit(self)
        service_id_input.setText(user.service_id)
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
        
        self.edit_user_controller.editUser(self.unique_user_id, username, service, service_id)
        self.closeWindow()

    
    def closeWindow(self):
        self.close()