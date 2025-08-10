from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QCheckBox

from view.left_pane.components.userListView import UserList

from controller.left_pane.leftPaneController import LeftPaneController

class LeftPane(QWidget):
    users = []
    
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        user_list = UserList()
        self.user_list = user_list
        main_layout.addWidget(user_list)
        
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
        
        main_layout.addLayout(user_buttons_layout)
        
        
        operation_button_layout = QHBoxLayout()
        full_url_check_box = QCheckBox("Full url check", self)
        
        get_user_urls_button = QPushButton("Download user's url", self)
        operation_button_layout.addWidget(get_user_urls_button)
        get_user_urls_button.clicked.connect(lambda: self.left_pane_controller.getUsersUrl(full_url_check_box) )
        
        get_all_user_urls_button = QPushButton("Download all user's url", self)
        operation_button_layout.addWidget(get_all_user_urls_button)
        get_all_user_urls_button.clicked.connect(lambda: self.left_pane_controller.getAllUsersUrl(full_url_check_box))
        
        operation_button_layout.addWidget(full_url_check_box)
        main_layout.addLayout(operation_button_layout)
        
        url_selection_layout = QHBoxLayout()
        show_selected_user_urls_button = QPushButton("Show select user/s urls", self)
        url_selection_layout.addWidget(show_selected_user_urls_button)
        show_selected_user_urls_button.clicked.connect(self.left_pane_controller.showSelectUsersUrls)
        
        show_all_urls_button = QPushButton("Show all users url", self)
        url_selection_layout.addWidget(show_all_urls_button)
        show_all_urls_button.clicked.connect(self.left_pane_controller.showAllUsersUrls)
        
        show_not_visited_urls_button = QPushButton("Show not visited urls", self)
        url_selection_layout.addWidget(show_not_visited_urls_button)
        show_not_visited_urls_button.clicked.connect(self.left_pane_controller.showNotVisitedUrls)
        
        main_layout.addLayout(url_selection_layout)
        
        self.left_pane_controller.updateUserList()
        