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

    def _setup_logging(self) -> None:
        """Configure application logging."""
        try:
            # Try to create file handler, fall back to console only if it fails
            handlers = [logging.StreamHandler()]
            try:
                handlers.append(logging.FileHandler('kemono_tracker.log'))
            except (OSError, PermissionError):
                # If we can't create log file, just use console
                pass
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=handlers,
                force=True  # Override any existing configuration
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("Application starting...")
        except Exception as e:
            # If logging setup fails completely, create a minimal logger
            self.logger = logging.getLogger(__name__)
            print(f"Logging setup failed: {e}")
            print("Application starting...")

    def _init_ui(self) -> None:
        """Initialize the user interface components."""
        try:
            # Create main panes with individual error handling
            try:
                print("Creating left pane...")
                self.left_pane = LeftPane()
                print("Left pane created successfully")
            except Exception as e:
                print(f"Failed to create left pane: {e}")
                raise
            
            try:
                print("Creating right pane...")
                self.right_pane = RightPane()
                print("Right pane created successfully")
            except Exception as e:
                print(f"Failed to create right pane: {e}")
                raise
            
            # Connect the panes so left pane can update right pane
            try:
                print("Connecting panes...")
                self._connect_panes()
                print("Panes connected successfully")
            except Exception as e:
                print(f"Failed to connect panes: {e}")
                raise
            
            # Create splitter with proper orientation
            print("Creating splitter...")
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
            self.setGeometry(100, 100, 800, 600)  # Default size and position
            
            # Set application icon if available
            try:
                icon_path = Path('assets/icon.png')
                if icon_path.exists():
                    self.setWindowIcon(QIcon(str(icon_path)))
            except Exception as e:
                # Icon loading failed, continue without icon
                print(f"Failed to load application icon: {e}")
                
            print("UI initialization completed successfully")
                
        except Exception as e:
            error_msg = f"Failed to initialize UI: {e}"
            print(error_msg)
            try:
                self.logger.error(error_msg)
            except:
                pass
            try:
                self._show_error("Initialization Error", f"Failed to initialize application: {e}")
            except:
                pass
            raise

    def _connect_panes(self) -> None:
        """Connect the left and right panes for communication."""
        # Set the right pane's URL list in the left pane controller
        self.left_pane.left_pane_controller.right_pane_url_list = self.right_pane.url_list
        
        # Set the right pane controller in the left pane controller for filter management
        self.left_pane.left_pane_controller.right_pane_controller = self.right_pane.right_pane_controller
        
        # Connect double-click signal from user list to show URLs
        self.left_pane.user_list.itemDoubleClicked.connect(self._on_user_double_clicked)

    def _on_user_double_clicked(self) -> None:
        """Handle double-click on user list to show their URLs."""
        try:
            print("=== Double-click on user detected ===")
            self.logger.info("User double-clicked, attempting to show URLs")
            self.left_pane.left_pane_controller.showSelectUsersUrls()
            self.status_bar.showMessage("Loaded URLs for selected user", 2000)
            print("=== User URLs loaded successfully ===")
        except Exception as e:
            error_msg = f"Error loading user URLs: {e}"
            print(f"=== ERROR: {error_msg} ===")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            self.logger.error(error_msg)
            self._show_error("Error", f"Failed to load user URLs: {e}")



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



    def closeEvent(self, event) -> None:
        """Handle application close event."""
        try:
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
    
    # Set application style and force light mode
    app.setStyle('Fusion')
    
    # Force light palette to prevent dark mode
    from PyQt6.QtGui import QPalette, QColor
    light_palette = QPalette()
    
    # Set light colors
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
    light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(light_palette)
    
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
        error_msg = f"Fatal error: {e}"
        print(error_msg)  # Always print to console
        try:
            logging.error(error_msg)
        except:
            pass  # Ignore logging errors
        
        try:
            if 'app' in locals():
                QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {e}")
        except:
            pass  # Ignore message box errors
        
        return 1


if __name__ == '__main__':
    sys.exit(main())
