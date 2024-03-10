from PyQt6.QtWidgets import QTableWidget , QTableWidgetItem, QAbstractItemView, QVBoxLayout, QWidget, QLabel

from model.urlModel import Url, values_names_to_display

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

        self.setColumnCount(len(values_names_to_display()))
        self.setHorizontalHeaderLabels(values_names_to_display())
        self.update()

    def update(self):
        urls = self.url_database_controller.getAllUrls()
        if not urls: return
        
        self.setRowCount(0)
        self.setRowCount(len(urls))
        
        for row, url in enumerate(urls):
            for col, val in enumerate(url.values_to_display()):
                table_item =  QTableWidgetItem(str(val))
                self.setItem(row, col, table_item)