from PyQt6.QtWidgets import QMessageBox, QPushButton

class WarningPopup:
    def __init__(self, warning_message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(warning_message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg_box.exec()