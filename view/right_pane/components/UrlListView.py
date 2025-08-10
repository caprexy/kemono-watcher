from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidget , QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from model.urlModel import Url, values_names_to_display, visited_text, urlValueIndexes

from controller.database.urlDatabaseController import UrlDatabaseController

class UrlListView(QTableWidget):
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
        
        self.update()

    def update(self, urls=None):
        if not urls:
            urls = self.url_database_controller.getAllUrls()
        
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
        # resort the columns if sorted
        current_column = self.horizontalHeader().sortIndicatorSection()
        current_order = self.horizontalHeader().sortIndicatorOrder()
        self.sortItems(current_column, current_order)
        
    
    def set_row_background_color(self, table_widget:QTableWidget, row, color):
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            if item is not None:
                item.setBackground(color)