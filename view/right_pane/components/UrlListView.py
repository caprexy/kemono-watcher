from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import QTableWidget , QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QLabel, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from model.urlModel import Url, values_names_to_display, visited_text, urlValueIndexes
import webbrowser

from controller.database.urlDatabaseController import UrlDatabaseController

class UrlListView(QTableWidget):
    # Custom signal for when a URL row is clicked to show user's URLs
    userUrlsRequested = pyqtSignal(str, str)  # service, service_id
    # Custom signal for when unvisited URLs are requested for a user
    userUnvisitedUrlsRequested = pyqtSignal(str, str)  # service, service_id
    # Custom signal for when URLs are flipped via context menu
    urlsFlipped = pyqtSignal()
    
    # Ensure is singleton
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UrlListView, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__()
        
        self.url_database_controller = UrlDatabaseController()

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        header_vals = values_names_to_display()
        self.setColumnCount(len(header_vals))
        self.setHorizontalHeaderLabels(header_vals)
        self.setColumnHidden(len(header_vals)-1, True)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setSortingEnabled(True)
        
        # Enable context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        # Initialize with empty data to avoid database issues during startup
        # Initialize with empty data to avoid database issues during startup
        try:
            self.update()
        except Exception:
            # Set empty table if update fails
            self.setRowCount(0)

    def update(self, urls=None):
        if not urls:
            urls = self.url_database_controller.getAllUrls()
        
        # Sort URLs to prioritize unvisited ones at the top
        urls = self._sort_urls_by_visited_status(urls)
        
        self.setRowCount(0)
        self.setRowCount(len(urls))

        self.setSortingEnabled(False) #https://stackoverflow.com/questions/7960505/strange-qtablewidget-behavior-not-all-cells-populated-after-sorting-followed-b
        
        for row, url in enumerate(urls):
            visited = False
            for col, val in enumerate(url.values_to_display()):
                if val is visited_text:
                    visited = True
                if type(val) is int:
                    table_item =  QTableWidgetItem()
                    table_item.setData(Qt.ItemDataRole.DisplayRole, val)
                else:
                    table_item =  QTableWidgetItem(str(val))
                self.setItem(row, col, table_item)
                
            if visited:
                self.set_row_background_color(self, row, QColor(102, 204, 102))
            else:
                self.set_row_background_color(self, row, QColor(255, 102, 102))
                
        self.setSortingEnabled(True)
        # Don't auto-sort after loading since we want to maintain our custom order
        # Users can still manually sort by clicking column headers if needed
        
        # Scroll to the top after updating content
        self.scrollToTop()
        
    
    def _sort_urls_by_visited_status(self, urls):
        """Sort URLs to show unvisited ones first, then visited ones."""
        # Separate unvisited and visited URLs
        unvisited_urls = [url for url in urls if not url.visited]
        visited_urls = [url for url in urls if url.visited]
        
        # Sort each group by post_id with safe handling of prefixed IDs
        def safe_post_id_sort_key(url):
            """Extract numeric part from post_id for sorting, handling prefixes like 'p-'."""
            try:
                post_id = url.post_id
                if post_id is None:
                    return 0
                
                # Convert to string first in case it's already an int
                post_id_str = str(post_id)
                
                # Handle prefixed post IDs like 'p-34234'
                if post_id_str.startswith('p-'):
                    return int(post_id_str[2:])  # Remove 'p-' prefix
                elif '-' in post_id_str:
                    # Handle other dash-separated formats, use the numeric part
                    parts = post_id_str.split('-')
                    for part in parts:
                        if part.isdigit():
                            return int(part)
                    return 0
                else:
                    # Try direct conversion
                    return int(post_id_str)
            except (ValueError, TypeError, AttributeError):
                # If all else fails, return 0 for consistent sorting
                return 0
        
        unvisited_urls.sort(key=safe_post_id_sort_key, reverse=True)
        visited_urls.sort(key=safe_post_id_sort_key, reverse=True)
        
        return unvisited_urls + visited_urls

    def _show_context_menu(self, position):
        """Show context menu at the given position."""
        # Get the item at the position
        item = self.itemAt(position)
        if item is None:
            return
        
        # Get selected URLs
        selected_urls = self._get_selected_urls_for_context_menu()
        if not selected_urls:
            return
        
        # Get unique users from selected rows
        selected_users = self._get_selected_users_for_context_menu()
        
        # Create context menu
        menu = QMenu(self)
        
        # Show User Unvisited URLs action
        if len(selected_users) == 1:
            # Single user selected
            user_info = list(selected_users)[0]
            username, service, service_id = user_info
            
            show_user_unvisited_action = QAction(f"Show Unvisited URLs for {username}", self)
            show_user_unvisited_action.triggered.connect(lambda: self.userUnvisitedUrlsRequested.emit(service, service_id))
            menu.addAction(show_user_unvisited_action)
        elif len(selected_users) > 1:
            # Multiple users selected
            show_users_unvisited_action = QAction(f"Show Unvisited URLs for {len(selected_users)} Users", self)
            show_users_unvisited_action.triggered.connect(lambda: self._show_multiple_users_unvisited(selected_users))
            menu.addAction(show_users_unvisited_action)
        
        if selected_users:
            menu.addSeparator()
        
        # Determine text based on selection count
        url_count = len(selected_urls)
        if url_count == 1:
            open_text = "Open URL in Browser"
            copy_text = "Copy URL"
            flip_text = "Flip Visit Status"
        else:
            open_text = f"Open {url_count} URLs in Browser"
            copy_text = f"Copy {url_count} URLs"
            flip_text = f"Flip Visit Status ({url_count} URLs)"
        
        # Open URL(s) action
        open_url_action = QAction(open_text, self)
        open_url_action.triggered.connect(lambda: self._open_selected_urls_in_browser(selected_urls))
        menu.addAction(open_url_action)
        
        menu.addSeparator()
        
        # Flip URL status action
        flip_url_action = QAction(flip_text, self)
        flip_url_action.triggered.connect(lambda: self._flip_selected_urls_status(selected_urls))
        menu.addAction(flip_url_action)
        
        menu.addSeparator()
        
        # Copy URL(s) action
        copy_url_action = QAction(copy_text, self)
        copy_url_action.triggered.connect(lambda: self._copy_selected_urls_to_clipboard(selected_urls))
        menu.addAction(copy_url_action)
        
        # Show the menu at the cursor position
        menu.exec(self.mapToGlobal(position))

    def _get_selected_urls_for_context_menu(self):
        """Get URLs from selected rows for context menu actions."""
        selected_items = self.selectedItems()
        if not selected_items:
            return []
        
        # Get unique rows from selected items
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        
        # Extract URLs from selected rows
        urls = []
        for row in selected_rows:
            url_item = self.item(row, urlValueIndexes.Url.value)
            if url_item:
                urls.append(url_item.text())
        
        return urls

    def _get_selected_users_for_context_menu(self):
        """Get unique users from selected rows."""
        selected_items = self.selectedItems()
        if not selected_items:
            return set()
        
        # Get unique rows from selected items
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        
        # Extract unique users from selected rows
        users = set()
        for row in selected_rows:
            username_item = self.item(row, urlValueIndexes.Username.value)
            service_item = self.item(row, urlValueIndexes.Service.value)
            service_id_item = self.item(row, urlValueIndexes.Service_id.value)
            
            if username_item and service_item and service_id_item:
                username = username_item.text()
                service = service_item.text()
                service_id = service_id_item.text()
                users.add((username, service, service_id))
        
        return users

    def _get_selected_url_objects_for_context_menu(self):
        """Get URL objects from selected rows for database operations."""
        selected_items = self.selectedItems()
        if not selected_items:
            return []
        
        # Get unique rows from selected items
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        
        # Extract URL objects from selected rows
        url_objects = []
        for row in selected_rows:
            try:
                # Get all data from the row
                row_data = []
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item:
                        text = item.text()
                        # Convert visited status back to boolean
                        if col == urlValueIndexes.Visited.value:
                            text = True if text == visited_text else False
                        row_data.append(text)
                
                if len(row_data) >= len(urlValueIndexes):
                    url_obj = Url(*row_data)
                    url_objects.append(url_obj)
            except Exception as e:
                print(f"Error creating URL object from row {row}: {e}")
        
        return url_objects

    def _open_selected_urls_in_browser(self, urls):
        """Open the selected URLs in the default browser."""
        for url in urls:
            try:
                webbrowser.open(url, autoraise=True)
            except Exception as e:
                print(f"Failed to open URL {url}: {e}")

    def _copy_selected_urls_to_clipboard(self, urls):
        """Copy the selected URLs to the clipboard."""
        try:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            # Join multiple URLs with newlines
            clipboard.setText('\n'.join(urls))
        except Exception as e:
            print(f"Failed to copy URLs: {e}")

    def _show_multiple_users_unvisited(self, selected_users):
        """Show unvisited URLs for multiple selected users."""
        # For now, we'll emit a signal with the first user and handle multiple users in the controller
        # This is a simplified approach - you could extend this to handle multiple users properly
        if selected_users:
            first_user = list(selected_users)[0]
            username, service, service_id = first_user
            # For multiple users, we could create a new signal or handle it differently
            # For now, just show the first user's unvisited URLs
            self.userUnvisitedUrlsRequested.emit(service, service_id)

    def _flip_selected_urls_status(self, urls):
        """Flip the visit status of selected URLs and show all user URLs."""
        try:
            # Get URL objects for database operations
            url_objects = self._get_selected_url_objects_for_context_menu()
            
            # Flip each URL's status in the database
            for url_obj in url_objects:
                self.url_database_controller.flipUrl(url_obj)
            
            # Get the users from flipped URLs to show their all URLs
            selected_users = self._get_selected_users_for_context_menu()
            if len(selected_users) == 1:
                # Single user - show all their URLs
                user_info = list(selected_users)[0]
                username, service, service_id = user_info
                self.userUrlsRequested.emit(service, service_id)
            else:
                # Multiple users or no specific user - just refresh current filter
                self.urlsFlipped.emit()
            
        except Exception as e:
            print(f"Failed to flip URL status: {e}")

    def set_row_background_color(self, table_widget:QTableWidget, row, color):
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            if item is not None:
                item.setBackground(color)