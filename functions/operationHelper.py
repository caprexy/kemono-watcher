from . import databaseHelper
import threading

idEntryElement = None
selectedService = None
addUserResultEle = None
addButtonutton = None


def passElements(idEntryElementIn, selectedServiceIn, addUserResultEleIn, addButtonuttonIn):
    global idEntryElement, selectedService, addUserResultEle, addButtonutton

    selectedService = selectedServiceIn
    idEntryElement = idEntryElementIn
    addUserResultEle = addUserResultEleIn
    addButtonutton = addButtonuttonIn

    databaseHelper.initalizeDatabase(addUserResultEle, addButtonutton)

# actual operations
def addUser():
    addButtonutton["state"] = "disabled"
    global idEntryElement, selectedService, addUserResultEle
    user = idEntryElement.get()
    service =  selectedService.get()
    
    if(len(idEntryElement.get()) == 0):
        addUserResultEle.config(text="Missing Id!", bg = "red")
        return
    elif(databaseHelper.userExists(user, service)):
        addUserResultEle.config(text="User already exists!", bg = "red")
        return
    else:
        addUserResultEle.config(text="", bg = "#f0f0f0")
        threading.Thread(target=databaseHelper.writeUser, args=(user, service)).start()
    addButtonutton["state"] = "normal"

def getUpdates():
    print("a")
