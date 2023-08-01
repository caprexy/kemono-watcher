from . import databaseHelper
import threading

idEntryElement = None
selectedService = None
addUserResultEle = None
addButtonutton = None
knownPostsListVar = None
unknownPostsListVar = None

def passElements(idEntryElementIn, selectedServiceIn, addUserResultEleIn, addButtonuttonIn, knownPostsListVarIn, unknownPostsListVarIn):
    global idEntryElement, selectedService, addUserResultEle, addButtonutton, knownPostsListVar, unknownPostsListVar

    selectedService = selectedServiceIn
    idEntryElement = idEntryElementIn
    addUserResultEle = addUserResultEleIn
    addButtonutton = addButtonuttonIn
    knownPostsListVar = knownPostsListVarIn
    unknownPostsListVar = unknownPostsListVarIn
    
    databaseHelper.initalizeDatabase(addUserResultEle, addButtonutton)

# actual operations
def addUser():
    addButtonutton["state"] = "disabled"
    global idEntryElement, selectedService, addUserResultEle
    user = idEntryElement.get()
    service =  selectedService.get()
    
    if(len(idEntryElement.get()) == 0):
        addUserResultEle.config(text="Missing Id!", bg = "red")
    elif(databaseHelper.userExists(user, service)):
        addUserResultEle.config(text="User already exists!", bg = "red")
    else:
        addUserResultEle.config(text="", bg = "#f0f0f0")
        threading.Thread(target=databaseHelper.writeUser, args=(user, service)).start()
    addButtonutton["state"] = "normal"

def viewUserInfo():
    global idEntryElement, selectedService, addUserResultEle, knownPostsListVar, unknownPostsListVar

    user = idEntryElement.get()
    service =  selectedService.get()

    data = databaseHelper.getUserData(user, service)
    knownPostsListVar.set(data["checkedPostIds"])
    unknownPostsListVar.set(data["uncheckedPostIds"])
    

def updateDatabase():
    global idEntryElement, selectedService, addUserResultEle, knownPostsListVar, unknownPostsListVar

    user = idEntryElement.get()
    service =  selectedService.get()

    knownList = []
    unknownList = []

    if(len( knownPostsListVar.get()) != 0):
        knownList = knownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(knownList[-1] == ''): knownList.pop()
    if(len( unknownPostsListVar.get()) != 0):
        unknownList = unknownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(unknownList[-1] == ''): unknownList.pop()

    data = {"checkedPostIds":knownList,
            "uncheckedPostIds":unknownList}
    
    databaseHelper.updateUserData(user, service, data)
    databaseHelper.writeDatabase()

def getUpdates():
    print("a")
