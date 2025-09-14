from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QCheckBox

from view.left_pane.components.userListView import UserList

from controller.left_pane.leftPaneController import LeftPaneController

class LeftPane(QWidget):
    users = []
    
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Create user list and make it accessible
        self.user_list = UserList()
        main_layout.addWidget(self.user_list)
        
        # Create controller and make it accessible
        self.left_pane_controller = LeftPaneController(self.user_list)
        
        # Connect context menu signals
        self._connect_context_menu_signals()

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
        
        # Initialize user list
        try:
            self.left_pane_controller.updateUserList()
        except Exception:
            # Continue without initial user list data
            pass

    def _connect_context_menu_signals(self):
        """Connect context menu signals to controller methods."""
        self.user_list.showNotVisitedRequested.connect(
            self.left_pane_controller.showNotVisitedUrlsForSelectedUsers
        )
        self.user_list.downloadUserUrlsRequested.connect(
            self._handle_download_urls_request
        )

    def _handle_download_urls_request(self, full_check: bool):
        """Handle download URLs request from context menu."""
        # Create a temporary checkbox object to pass the full_check state
        class TempCheckBox:
            def __init__(self, checked: bool):
                self._checked = checked
            def isChecked(self):
                return self._checked
        
        temp_checkbox = TempCheckBox(full_check)
        self.left_pane_controller.getUsersUrl(temp_checkbox)
        