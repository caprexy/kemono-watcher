from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton

from view.left_pane.components.userListView import UserList

from controller.left_pane.leftPaneController import LeftPaneController

class LeftPane(QWidget):
    users = []
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        user_list = UserList()
        self.user_list = user_list
        layout.addWidget(user_list)
        
        self.left_pane_controller = LeftPaneController(user_list)

        user_buttons_layout = QHBoxLayout()

        add_user_button = QPushButton('Add User', self)
        user_buttons_layout.addWidget(add_user_button)
        add_user_button.clicked.connect(self.left_pane_controller.openAddUser)
        
        add_user_button = QPushButton('Edit User', self)
        user_buttons_layout.addWidget(add_user_button)
        add_user_button.clicked.connect(self.left_pane_controller.openEditUser)
        
        add_user_button = QPushButton('Delete User', self)
        user_buttons_layout.addWidget(add_user_button)
        add_user_button.clicked.connect(self.left_pane_controller.openDeleteUser)
        
        layout.addLayout(user_buttons_layout)
        
        self.left_pane_controller.updateUserList()