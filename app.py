#!/usr/bin/env python3
"""
Kemono Manual URL Tracker - Main Application Entry Point

A PyQt6-based application for tracking and managing Kemono URLs.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QVBoxLayout, 
    QWidget, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt, QSettings, QTimer
from PyQt6.QtGui import QIcon, QAction

from view.left_pane.leftPane import LeftPane
from view.right_pane.rightPane import RightPane


class KemonoTrackerApp(QMainWindow):
    """Main application window with two-pane layout for user and URL management."""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('KemonoTracker', 'MainApp')
        self.left_pane: Optional[LeftPane] = None
        self.right_pane: Optional[RightPane] = None
        self.splitter: Optional[QSplitter] = None
        
        self._setup_logging()
        self._init_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._restore_window_state()
        self._restore_table_column_sizes()
        
        # Auto-save timer for window state and column sizes
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self._save_all_settings)
        self.auto_save_timer.start(30000)  # Save every 30 seconds

    def _setup_logging(self) -> None:
        """Configure application logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kemono_tracker.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Application starting...")

    def _init_ui(self) -> None:
        """Initialize the user interface components."""
        try:
            # Create main panes
            self.left_pane = LeftPane()
            self.right_pane = RightPane()
            
            # Connect the panes so left pane can update right pane
            self._connect_panes()
            
            # Create splitter with proper orientation
            self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
            self.splitter.addWidget(self.left_pane)
            self.splitter.addWidget(self.right_pane)
            
            # Set initial splitter proportions (40% left, 60% right)
            self.splitter.setSizes([320, 480])
            self.splitter.setChildrenCollapsible(False)
            
            # Create central widget with layout
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.addWidget(self.splitter)
            
            self.setCentralWidget(central_widget)
            
            # Set window properties
            self.setWindowTitle('Kemono Manual URL Tracker')
            self.setMinimumSize(600, 400)
            
            # Set application icon if available
            icon_path = Path('assets/icon.png')
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
                
        except Exception as e:
            self.logger.error(f"Failed to initialize UI: {e}")
            self._show_error("Initialization Error", f"Failed to initialize application: {e}")

    def _connect_panes(self) -> None:
        """Connect the left and right panes for communication."""
        # Set the right pane's URL list in the left pane controller
        self.left_pane.left_pane_controller.right_pane_url_list = self.right_pane.url_list
        
        # Set the right pane controller in the left pane controller for filter management
        self.left_pane.left_pane_controller.right_pane_controller = self.right_pane.right_pane_controller
        
        # Connect double-click signal from user list to show URLs
        self.left_pane.user_list.itemDoubleClicked.connect(self._on_user_double_clicked)
        
        # Setup column size persistence for both tables
        self._setup_table_persistence()

    def _on_user_double_clicked(self) -> None:
        """Handle double-click on user list to show their URLs."""
        try:
            self.left_pane.left_pane_controller.showSelectUsersUrls()
            self.status_bar.showMessage("Loaded URLs for selected user", 2000)
        except Exception as e:
            self.logger.error(f"Error loading user URLs: {e}")
            self._show_error("Error", f"Failed to load user URLs: {e}")

    def _setup_table_persistence(self) -> None:
        """Setup column size persistence for tables."""
        # Connect signals to save column sizes when they change
        if self.left_pane and self.left_pane.user_list:
            header = self.left_pane.user_list.horizontalHeader()
            header.sectionResized.connect(self._save_user_table_column_sizes)
            
        if self.right_pane and self.right_pane.url_list:
            header = self.right_pane.url_list.horizontalHeader()
            header.sectionResized.connect(self._save_url_table_column_sizes)

    def _save_user_table_column_sizes(self) -> None:
        """Save user table column sizes."""
        try:
            if self.left_pane and self.left_pane.user_list:
                header = self.left_pane.user_list.horizontalHeader()
                column_sizes = []
                for i in range(header.count()):
                    column_sizes.append(header.sectionSize(i))
                self.settings.setValue("userTableColumnSizes", column_sizes)
        except Exception as e:
            self.logger.warning(f"Failed to save user table column sizes: {e}")

    def _save_url_table_column_sizes(self) -> None:
        """Save URL table column sizes."""
        try:
            if self.right_pane and self.right_pane.url_list:
                header = self.right_pane.url_list.horizontalHeader()
                column_sizes = []
                for i in range(header.count()):
                    column_sizes.append(header.sectionSize(i))
                self.settings.setValue("urlTableColumnSizes", column_sizes)
        except Exception as e:
            self.logger.warning(f"Failed to save URL table column sizes: {e}")

    def _restore_table_column_sizes(self) -> None:
        """Restore saved column sizes for tables."""
        try:
            # Restore user table column sizes
            if self.left_pane and self.left_pane.user_list:
                column_sizes = self.settings.value("userTableColumnSizes")
                if column_sizes:
                    header = self.left_pane.user_list.horizontalHeader()
                    for i, size in enumerate(column_sizes):
                        if i < header.count():
                            header.resizeSection(i, int(size))
            
            # Restore URL table column sizes
            if self.right_pane and self.right_pane.url_list:
                column_sizes = self.settings.value("urlTableColumnSizes")
                if column_sizes:
                    header = self.right_pane.url_list.horizontalHeader()
                    for i, size in enumerate(column_sizes):
                        if i < header.count():
                            header.resizeSection(i, int(size))
                            
        except Exception as e:
            self.logger.warning(f"Failed to restore table column sizes: {e}")

    def _setup_menu_bar(self) -> None:
        """Create and configure the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        reset_layout_action = QAction('&Reset Layout', self)
        reset_layout_action.triggered.connect(self._reset_layout)
        view_menu.addAction(reset_layout_action)
        
        reset_columns_action = QAction('Reset &Column Sizes', self)
        reset_columns_action.triggered.connect(self._reset_column_sizes)
        view_menu.addAction(reset_columns_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_status_bar(self) -> None:
        """Create and configure the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready", 2000)

    def _reset_layout(self) -> None:
        """Reset the splitter layout to default proportions."""
        if self.splitter:
            self.splitter.setSizes([320, 480])

    def _reset_column_sizes(self) -> None:
        """Reset column sizes to default values."""
        try:
            # Reset user table columns
            if self.left_pane and self.left_pane.user_list:
                header = self.left_pane.user_list.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
                header.setStretchLastSection(True)
                # Set some reasonable default widths
                default_widths = [80, 150, 100, 100]  # ID, Username, Service, Service_ID
                for i, width in enumerate(default_widths):
                    if i < header.count():
                        header.resizeSection(i, width)
            
            # Reset URL table columns  
            if self.right_pane and self.right_pane.url_list:
                header = self.right_pane.url_list.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
                header.setStretchLastSection(True)
                # Set reasonable defaults for URL table
                default_widths = [120, 80, 80, 80, 300, 100, 120]  # Username, Service, Service_ID, Post_ID, URL, Visited, Visited_time
                for i, width in enumerate(default_widths):
                    if i < header.count() - 1:  # Don't resize the hidden last column
                        header.resizeSection(i, width)
            
            # Clear saved column sizes
            self.settings.remove("userTableColumnSizes")
            self.settings.remove("urlTableColumnSizes")
            
            self.status_bar.showMessage("Column sizes reset to defaults", 2000)
            
        except Exception as e:
            self.logger.error(f"Failed to reset column sizes: {e}")
            self._show_error("Error", f"Failed to reset column sizes: {e}")

    def _show_about(self) -> None:
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About Kemono Tracker",
            "Kemono Manual URL Tracker\n\n"
            "A tool for managing and tracking Kemono URLs.\n"
            "Built with PyQt6."
        )

    def _show_error(self, title: str, message: str) -> None:
        """Display an error message to the user."""
        QMessageBox.critical(self, title, message)

    def _save_window_state(self) -> None:
        """Save the current window state and geometry."""
        try:
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("windowState", self.saveState())
            if self.splitter:
                self.settings.setValue("splitterSizes", self.splitter.sizes())
        except Exception as e:
            self.logger.warning(f"Failed to save window state: {e}")

    def _save_all_settings(self) -> None:
        """Save all application settings including window state and column sizes."""
        self._save_window_state()
        self._save_user_table_column_sizes()
        self._save_url_table_column_sizes()

    def _restore_window_state(self) -> None:
        """Restore the saved window state and geometry."""
        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
            else:
                # Default size and position
                self.setGeometry(100, 100, 800, 600)
                
            window_state = self.settings.value("windowState")
            if window_state:
                self.restoreState(window_state)
                
            splitter_sizes = self.settings.value("splitterSizes")
            if splitter_sizes and self.splitter:
                self.splitter.setSizes([int(size) for size in splitter_sizes])
                
        except Exception as e:
            self.logger.warning(f"Failed to restore window state: {e}")
            self.setGeometry(100, 100, 800, 600)

    def closeEvent(self, event) -> None:
        """Handle application close event."""
        try:
            self._save_all_settings()
            self.logger.info("Application closing...")
            event.accept()
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
            event.accept()


def setup_application() -> QApplication:
    """Configure and return the QApplication instance."""
    app = QApplication(sys.argv)
    app.setApplicationName("Kemono Tracker")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("KemonoTracker")
    
    # Set application style
    app.setStyle('Fusion')
    
    return app


def main() -> int:
    """Main application entry point."""
    try:
        app = setup_application()
        
        # Create and show main window
        window = KemonoTrackerApp()
        window.show()
        
        # Start event loop
        return app.exec()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        if 'app' in locals():
            QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
