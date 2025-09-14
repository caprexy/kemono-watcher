from PyQt6.QtCore import QObject, QThread, pyqtSignal
import requests, time, json

from controller.database.urlDatabaseController import UrlDatabaseController

from model.userModel import User
from model.urlModel import Url

from view.popups import WarningPopup

class KemonoApiController:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.database_controller = UrlDatabaseController()
    
    def scanUserUrls(self, user:User, update_dialogue_funct, full_url_check, close_signal, finish_popup = True):
        worker_thread = WorkerThread(self.parent, 
                                    user.service, 
                                    user.service_id, 
                                    user.username,
                                    self.database_controller,
                                    full_url_check)
        worker_thread.update_dialog.connect(
            lambda new_urls, total_urls: update_dialogue_funct(new_urls, total_urls)
        )
        close_signal.connect(worker_thread.terminate)
        if finish_popup:
            worker_thread.finished.connect(lambda : WarningPopup("Finished " + user.username + " from " + user.service))
        worker_thread.start()

class WorkerThread(QThread):
    update_dialog = pyqtSignal(int, int) # new, total urls
    finished = pyqtSignal()
    
    def __init__(self, parent, service:str, service_id:int, username:str, database_controller:UrlDatabaseController, full_url_check:bool) -> None:
        super().__init__(parent)
        self.service = service
        self.service_id = service_id
        self.database_controller = database_controller
        self.username = username
        self.full_url_check = full_url_check
        
    def run(self):
        step = -50
        step_size = 50
        res_list = [1]
        while res_list != []:

            url = f"https://kemono.cr/api/v1/{self.service}/user/{self.service_id}/posts?o="
            headers = {
                "Accept": "text/css",
                "User-Agent": "Mozilla/5.0"  # mimic a browser
            }
            step += step_size
            if (not self.full_url_check) and (step > step_size * 4):
                break
            
            try: 
                response = requests.get(url+str(step), headers=headers)
                while response.status_code != 200:
                    time.sleep(1)
                    response = requests.get(url+str(step))
            except requests.exceptions.ConnectionError as e:
                print("Connection error:", e)
            except requests.exceptions.Timeout as e:
                print("Timeout error:", e)
            except requests.exceptions.HTTPError as e:
                print("HTTP error:", e)
                
            total_urls = 0
            new_urls = 0
            if response.status_code == 200:
                res_list = response.json()
                for result in res_list:
                    post_id = result["id"]
                    resUrl = postUrlMaker(self.service, self.service_id, post_id)
                    if not self.database_controller.doesUrlExist(resUrl):
                        self.database_controller.addUrl(url=resUrl, 
                                                        visited=False, 
                                                        visited_time=None, 
                                                        service=self.service, 
                                                        service_id=self.service_id, 
                                                        username=self.username, 
                                                        post_id=post_id)
                        new_urls += 1
                    total_urls += 1
                self.update_dialog.emit(new_urls, total_urls)
            else:
                # Print an error message
                print(f"Error: {response}")
            pass
        
        self.finished.emit()

def postUrlMaker(service, service_id, post_id):
    return f"https://kemono.cr/{service}/user/{service_id}/post/{post_id}"

def postUrlDecrypter(url):
    parts = url.split("/")
    
    if len(parts) == 8 and parts[2] == "kemono.cr" and parts[4] == "user":
        service = parts[3]
        service_id = parts[5]
        post_id = parts[7]
        return service, service_id, post_id
    else:
        # Return None or raise an exception for invalid URLs
        return None
