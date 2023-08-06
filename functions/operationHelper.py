from . import databaseHelper
import threading

idEntryElement = None
selectedService = None

viewAddIdStatusLabel = None
addButtonutton = None
knownPostsListVar = None
unknownPostsListVar = None

databaseHelper.initalizeDatabase()

def setServiceAndUserId(selectedServiceVar, userIdEle):
    global idEntryElement, selectedService
    selectedService = selectedServiceVar
    idEntryElement = userIdEle

def setViewAddIdStatusLabel(viewAddIdStatusLabelIn):
    global viewAddIdStatusLabel
    viewAddIdStatusLabel = viewAddIdStatusLabelIn

def setAddButton(addButtonuttonIn):
    global addButtonutton
    addButtonutton = addButtonuttonIn

def setKnownPostVar(knownPostsListVarIn):
    global knownPostsListVar

    knownPostsListVar = knownPostsListVarIn

def setUnknownPostVar(unknownPostsListVarIn):
    global unknownPostsListVar
    
    unknownPostsListVar = unknownPostsListVarIn

# actual operations
def addUser():
    addButtonutton["state"] = "disabled"
    global idEntryElement, selectedService, viewAddIdStatusLabel
    user = idEntryElement.get()
    service =  selectedService.get()
    
    if(len(idEntryElement.get()) == 0):
        viewAddIdStatusLabel.config(text="Missing Id!", bg = "red")
    elif(databaseHelper.userExists(user, service)):
        viewAddIdStatusLabel.config(text="User already exists!", bg = "red")
    else:
        viewAddIdStatusLabel.config(text="", bg = "#f0f0f0")
        threading.Thread(target=databaseHelper.writeUser, args=(user, service)).start()
    addButtonutton["state"] = "normal"

def viewUserInfo():
    global idEntryElement, selectedService, viewAddIdStatusLabel, knownPostsListVar, unknownPostsListVar

    user = idEntryElement.get()
    service =  selectedService.get()

    data = databaseHelper.getUserData(user, service)
    if(data == []):
        viewAddIdStatusLabel.config(text="User couldnt find user!", bg = "red")
        return
    
    knownPostsListVar.set(data["checkedPostIds"])
    unknownPostsListVar.set(data["uncheckedPostIds"])
    

def updateDatabase():
    global idEntryElement, selectedService, viewAddIdStatusLabel, knownPostsListVar, unknownPostsListVar

    user = idEntryElement.get()
    service =  selectedService.get()

    knownList = []
    unknownList = []

    knownList = formatStrVarToList(knownPostsListVar)
    unknownList = formatStrVarToList(unknownPostsListVar)

    
    databaseHelper.updateUserData(user, service, knownList, unknownList)
    databaseHelper.writeDatabase()

def formatStrVarToList(strVar):
    finList = []
    if(len( strVar.get()) != 0):
        finList = strVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(finList[-1] == ''): finList.pop()
    return finList
