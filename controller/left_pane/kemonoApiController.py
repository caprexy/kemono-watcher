from PyQt6.QtCore import QObject, QThread, pyqtSignal
import requests

from controller.database.urlDatabaseController import UrlDatabaseController
from model.userModel import User
from model.urlModel import Url

class KemonoApiController:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.database_controller = UrlDatabaseController()
    
    def generateUserUrls(self, user:User, update_dialogue_funct):
        worker_thread = WorkerThread(self.parent, 
                                    user.service, 
                                    user.service_id, 
                                    user.username,
                                    self.database_controller)
        worker_thread.update_dialog.connect(
            lambda new_urls, total_urls: update_dialogue_funct(new_urls, total_urls)
        )
        worker_thread.start()

class WorkerThread(QThread):
    update_dialog = pyqtSignal(int, int) # new, total urls
    
    def __init__(self, parent, service:str, service_id:int, username:str, database_controller:UrlDatabaseController) -> None:
        super().__init__(parent)
        self.service = service
        self.service_id = service_id
        self.database_controller = database_controller
        self.username = username
        
    def run(self):
        
        step = -50
        res_list = [1]
        while res_list != []:
            request = "https://kemono.su/api/v1/" + self.service + \
                        "/user/" + str(self.service_id) + "?o="
            step += 50
            response = requests.get(request+str(step))
            total_urls = 0
            new_urls = 0
            if response.status_code == 200:
                res_list = response.json()
                for result in res_list:
                    id = result["id"]
                    resUrl = f"https://kemono.su/{self.service}/user/{self.service_id}/post/{id}"
                    if not self.database_controller.doesUrlExist(resUrl):
                        self.database_controller.addUrl(resUrl, False, None, self.service, self.service_id, self.username)
                        new_urls += 1
                    total_urls += 1
                self.update_dialog.emit(new_urls, total_urls)
            else:
                # Print an error message
                print(f"Error: {response.status_code}")
            pass