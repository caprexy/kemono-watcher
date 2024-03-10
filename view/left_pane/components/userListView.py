from PyQt6.QtWidgets import QTableWidget , QTableWidgetItem, QAbstractItemView, QVBoxLayout, QWidget, QLabel

from model.userModel import User, values_names_to_display

class UserList(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(len(values_names_to_display()))
        self.setHorizontalHeaderLabels(values_names_to_display())
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cellClicked.connect(self.on_cell_clicked)

        
    def update(self, users:[User]):
        if not users: return
        
        self.setRowCount(0)
        self.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, val in enumerate(user.values_to_display()):
                table_item =  QTableWidgetItem(str(val))
                self.setItem(row, col, table_item)
                
    def on_cell_clicked(self, row, col):
        # Custom slot to handle the cellClicked event
        print(f'Cell clicked at: ({row}, {col})')