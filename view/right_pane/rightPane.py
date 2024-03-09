from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class RightPane(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create buttons
        btn1 = QPushButton('Button 1', self)
        btn2 = QPushButton('Button 2', self)
        btn3 = QPushButton('Button 3', self)
        btn4 = QPushButton('Button 4', self)

        # Connect buttons to custom functions
        btn1.clicked.connect(self.on_button1_click)
        btn2.clicked.connect(self.on_button2_click)
        btn3.clicked.connect(self.on_button3_click)
        btn4.clicked.connect(self.on_button4_click)

        # Create layout and add buttons
        layout = QVBoxLayout(self)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)

        # Set layout for the widget
        self.setLayout(layout)


    # Custom functions for button clicks
    def on_button1_click(self):
        print("Button 1 clicked")

    def on_button2_click(self):
        print("Button 2 clicked")

    def on_button3_click(self):
        print("Button 3 clicked")

    def on_button4_click(self):
        print("Button 4 clicked")
