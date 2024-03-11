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
        
        url_buttons_layout = QHBoxLayout()
        add_url_button = QPushButton('Add url', self)
        url_buttons_layout.addWidget(add_url_button)
        add_url_button.clicked.connect(self.right_pane_controller.addUrl)
        
        delete_url_button = QPushButton('Delete url', self)
        url_buttons_layout.addWidget(delete_url_button)
        delete_url_button.clicked.connect(self.right_pane_controller.deleteUrl)
        
        main_layout.addLayout(url_buttons_layout)
        
        visit_url_buttons = QHBoxLayout()
        open_urls_button = QPushButton('Open urls', self)
        visit_url_buttons.addWidget(open_urls_button)
        open_urls_button.clicked.connect(self.right_pane_controller.openUrls)
        
        visit_urls_button = QPushButton('Flip url visit status', self)
        visit_url_buttons.addWidget(visit_urls_button)
        visit_urls_button.clicked.connect(self.right_pane_controller.flipUrl)
        
        main_layout.addLayout(visit_url_buttons)
