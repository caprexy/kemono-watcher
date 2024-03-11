from PyQt6.QtWidgets import QTableWidget , QTableWidgetItem, QAbstractItemView,  QHeaderView, QAbstractScrollArea, QSizePolicy
from model.userModel import User, values_names_to_display

class UserList(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(len(values_names_to_display()))
        self.setHorizontalHeaderLabels(values_names_to_display())
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSortingEnabled(True)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update(self, users:[User]):
        if not users: return
        
        self.setRowCount(0)
        self.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, val in enumerate(user.values_to_display()):
                table_item =  QTableWidgetItem(str(val))
                self.setItem(row, col, table_item)
        
