from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton

from view.right_pane.components.UrlListView import UrlListView

from controller.right_pane.rightPaneController import RightPaneController

class RightPane(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        
        url_list = UrlListView()
        self.url_list = url_list
        main_layout.addWidget(self.url_list)
        
        self.right_pane_controller = RightPaneController(url_list)
        
        # Connect URL click signal to show user URLs
        self.url_list.userUrlsRequested.connect(self.right_pane_controller.showUserUrls)
        
        # Connect unvisited URLs signal to show user's unvisited URLs
        self.url_list.userUnvisitedUrlsRequested.connect(self.right_pane_controller.showUserUnvisitedUrls)
        
        # Connect URL flip signal to refresh current filter and user list
        self.url_list.urlsFlipped.connect(self.right_pane_controller._refresh_after_url_change)
        
        # Flip URL status button - prominent at the top
        flip_urls_button = QPushButton('Flip URL Visit Status', self)
        flip_urls_button.clicked.connect(self.right_pane_controller.flipUrl)
        
        # Style the flip button - larger and orange
        flip_urls_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #FF7F00;
            }
            QPushButton:pressed {
                background-color: #E67E00;
            }
        """)
        
        main_layout.addWidget(flip_urls_button)
        
        # URL management buttons
        url_buttons_layout = QHBoxLayout()
        add_url_button = QPushButton('Add url', self)
        url_buttons_layout.addWidget(add_url_button)
        add_url_button.clicked.connect(self.right_pane_controller.addUrl)
        
        delete_url_button = QPushButton('Delete url', self)
        url_buttons_layout.addWidget(delete_url_button)
        delete_url_button.clicked.connect(self.right_pane_controller.deleteUrl)
        
        main_layout.addLayout(url_buttons_layout)
        
        # Other action buttons
        action_buttons_layout = QHBoxLayout()
        open_urls_button = QPushButton('Open urls', self)
        action_buttons_layout.addWidget(open_urls_button)
        open_urls_button.clicked.connect(self.right_pane_controller.openUrls)
        
        main_layout.addLayout(action_buttons_layout)
