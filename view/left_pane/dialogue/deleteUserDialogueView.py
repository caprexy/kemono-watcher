import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox

from controller.left_pane.dialogue.deleteUserController import DeleteUserController

from view.popups import WarningPopup
import view.left_pane.constants as constants

from model.userModel import User

class DeleteUserDialogue(QDialog):
    def __init__(self, 
                user:User
                ):
        super().__init__()
    
        self.unique_user_id = user.id
        
        self.delete_user_controller = DeleteUserController()
        
        # Set window properties
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('User Input Dialog')
        
        
        ## Widgets
        deleting_label = QLabel(f"DELETING THIS USER")
        main_layout.addWidget(deleting_label)
        
        username_label = QLabel(f"Username: {user.username}")
        main_layout.addWidget(username_label)
        
        service_label = QLabel(f"Service: {user.service}")
        main_layout.addWidget(service_label)
        
        service_id_label = QLabel(f"Service ID: {user.service_id}")
        main_layout.addWidget(service_id_label)
        
        accept_button = QPushButton("Accept")
        accept_button.clicked.connect(self.acceptClicked)
        main_layout.addWidget(accept_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.closeWindow)
        main_layout.addWidget(close_button)
        
        
    def acceptClicked(self):
        self.delete_user_controller.deleteUser(self.unique_user_id)
        self.closeWindow()

    
    def closeWindow(self):
        self.close()