from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QProgressDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from model.userModel import User

from view.right_pane.components.UrlListView import UrlListView
from view.popups import WarningPopup

from controller.left_pane.kemonoApiController import KemonoApiController

class UrlsManager:
    def downloadUrls(self, user:User, url_list_view:UrlListView, full_url_check: bool):
        dialogue = DownloadingUrlsDialogue(url_list_view)
        
        controller = KemonoApiController(dialogue)
        controller.scanUserUrls(user, dialogue.update_url_label, full_url_check, dialogue.finished)
        dialogue.exec()

    def downloadAllUserUrls(self, users:[User], url_list_view:UrlListView, full_url_check: bool):
        dialogue = DownloadingUrlsDialogue(url_list_view)
        controller = KemonoApiController(dialogue)
        for user in users:
            controller.scanUserUrls(user, dialogue.update_url_label, full_url_check,  dialogue.finished, finish_popup = False)
        dialogue.exec()

class DownloadingUrlsDialogue(QDialog):
    total_new_urls = 0
    total_total_urls = 0
    def __init__(self, url_list_view:UrlListView):
        super().__init__()

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        status_label = QLabel("Added 0 new urls, processed 0 urls total")
        self.status_label = status_label
        main_layout.addWidget(status_label)

        buttons_layout = QHBoxLayout()
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        main_layout.addLayout(buttons_layout)
        self.url_list_view = url_list_view
        
    def update_url_label(self, new_urls:int, total_urls:int):
        self.total_new_urls = self.total_new_urls+new_urls
        self.total_total_urls = self.total_total_urls+total_urls
        self.status_label.setText(f"Added {self.total_new_urls} new urls, processed {self.total_total_urls} urls total")
        self.url_list_view.update()
        