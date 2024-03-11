from PyQt6.QtWidgets import QMessageBox, QPushButton

class WarningPopup:
    def __init__(self, warning_message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(warning_message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg_box.exec()
        
class ConfirmPopup:
    def __init__(self, confirm_message) -> None:
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Icon.Question)
        confirm_dialog.setWindowTitle("Confirm Action")
        confirm_dialog.setText("Do you want to perform this action?: "+ confirm_message)
        confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm_dialog.setDefaultButton(QMessageBox.StandardButton.No)
        self.confirm_dialog = confirm_dialog
        
    
    def exec(self):
        return self.confirm_dialog.exec()