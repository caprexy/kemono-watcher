from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, 
    QAbstractScrollArea, QSizePolicy, QMenu, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from model.userModel import User, values_names_to_display

class UserList(QTableWidget):
    # Custom signals for context menu actions
    showNotVisitedRequested = pyqtSignal()
    downloadUserUrlsRequested = pyqtSignal(bool)  # bool for full_url_check
    
    def __init__(self):
        super().__init__()

        self.setColumnCount(len(values_names_to_display()))
        self.setHorizontalHeaderLabels(values_names_to_display())
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSortingEnabled(True)
        
        # Allow interactive column resizing while keeping last column stretched
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        
        # Enable context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def update(self, users:[User]):
        if not users: 
            return
        
        self.setRowCount(0)
        self.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, val in enumerate(user.values_to_display()):
                table_item = QTableWidgetItem(str(val))
                self.setItem(row, col, table_item)

    def _show_context_menu(self, position):
        """Show context menu at the given position."""
        # Only show menu if there's a selection
        if not self.selectedRanges():
            return
            
        menu = QMenu(self)
        
        # Show not visited URLs action
        show_not_visited_action = QAction("Show Not Visited URLs for Selected User(s)", self)
        show_not_visited_action.triggered.connect(self._on_show_not_visited)
        menu.addAction(show_not_visited_action)
        
        menu.addSeparator()
        
        # Download user URLs submenu
        download_menu = menu.addMenu("Download User URLs")
        
        # Normal download
        download_normal_action = QAction("Download URLs", self)
        download_normal_action.triggered.connect(lambda: self._on_download_urls(False))
        download_menu.addAction(download_normal_action)
        
        # Full URL check download
        download_full_action = QAction("Download URLs (Full Check)", self)
        download_full_action.triggered.connect(lambda: self._on_download_urls(True))
        download_menu.addAction(download_full_action)
        
        # Show the menu at the cursor position
        menu.exec(self.mapToGlobal(position))

    def _on_show_not_visited(self):
        """Handle show not visited URLs action."""
        self.showNotVisitedRequested.emit()

    def _on_download_urls(self, full_check: bool):
        """Handle download URLs action."""
        self.downloadUserUrlsRequested.emit(full_check)
        
