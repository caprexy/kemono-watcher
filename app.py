import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QSplitter, QVBoxLayout, QWidget

from view.left_pane.leftPane import LeftPane
from view.right_pane.rightPane import RightPane

class TwoPaneApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        left_pane = LeftPane()
        right_pane = RightPane()

        # Create a splitter widget
        splitter = QSplitter(self)
        splitter.addWidget(left_pane)
        splitter.addWidget(right_pane)

        # Set the layout for the central widget
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(splitter)

        # Set the central widget and layout
        self.setCentralWidget(central_widget)

        # Set window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Kemono Manual URL Tracker')

def main():
    app = QApplication(sys.argv)
    window = TwoPaneApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
