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
        dialogue = DownloadingAllUsersUrlsDialogue(users, url_list_view, full_url_check)
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


class DownloadingAllUsersUrlsDialogue(QDialog):
    def __init__(self, users:[User], url_list_view:UrlListView, full_url_check: bool):
        super().__init__()
        self.users = users
        self.url_list_view = url_list_view
        self.full_url_check = full_url_check
        self.current_user_index = 0
        self.total_new_urls = 0
        self.total_total_urls = 0
        self.completed_users = 0
        
        self.setWindowTitle("Downloading All Users URLs")
        self.setModal(True)
        self.resize(400, 150)
        
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Current user label
        self.current_user_label = QLabel("Preparing to download...")
        main_layout.addWidget(self.current_user_label)
        
        # Progress label
        self.progress_label = QLabel(f"User 0 of {len(users)}")
        main_layout.addWidget(self.progress_label)

        # Status label
        self.status_label = QLabel("Added 0 new urls, processed 0 urls total")
        main_layout.addWidget(self.status_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setEnabled(False)  # Disabled until completion
        
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        main_layout.addLayout(buttons_layout)
        
        # Start downloading
        self.start_next_user()
        
    def start_next_user(self):
        """Start downloading for the next user."""
        if self.current_user_index >= len(self.users):
            self.download_completed()
            return
            
        user = self.users[self.current_user_index]
        self.current_user_label.setText(f"Downloading: {user.username} ({user.service})")
        self.progress_label.setText(f"User {self.current_user_index + 1} of {len(self.users)}")
        
        # Create controller and start download
        controller = KemonoApiController(self)
        controller.scanUserUrls(
            user, 
            self.update_url_label, 
            self.full_url_check, 
            self.user_finished, 
            finish_popup=False
        )
    
    def update_url_label(self, new_urls:int, total_urls:int):
        """Update the progress labels."""
        self.total_new_urls += new_urls
        self.total_total_urls += total_urls
        self.status_label.setText(f"Added {self.total_new_urls} new urls, processed {self.total_total_urls} urls total")
        self.url_list_view.update()
        
    def user_finished(self):
        """Called when current user download is finished."""
        self.completed_users += 1
        self.current_user_index += 1
        
        # Start next user or finish
        self.start_next_user()
        
    def download_completed(self):
        """Called when all users are processed."""
        self.current_user_label.setText("✅ All downloads completed!")
        self.progress_label.setText(f"Completed {self.completed_users} users")
        self.ok_button.setEnabled(True)
        self.cancel_button.setText("Close")
        
        # Show completion popup
        from view.popups import WarningPopup
        WarningPopup(f"Finished downloading URLs for all {self.completed_users} users!\n"
                    f"Added {self.total_new_urls} new URLs, processed {self.total_total_urls} total.")
        
    def finished(self):
        """Signal slot for compatibility."""
        pass
        