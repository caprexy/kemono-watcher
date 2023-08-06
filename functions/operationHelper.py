from . import databaseHelper
import threading

idEntryElement = None
selectedService = None

viewAddIdStatusLabel = None
addButtonutton = None
knownPostsListVar = None
unknownPostsListVar = None

knownPostsListbox = None
unknownPostsListbox = None

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

def setKnownPostVarList(knownPostsListVarIn, knownPostsListboxIn):
    global knownPostsListVar, knownPostsListbox

    knownPostsListVar = knownPostsListVarIn
    knownPostsListbox = knownPostsListboxIn

def setUnknownPostVarList(unknownPostsListVarIn, unknownPostsListboxIn):
    global unknownPostsListVar, unknownPostsListbox
    
    unknownPostsListVar = unknownPostsListVarIn
    unknownPostsListbox = unknownPostsListboxIn

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


def moveKnownToUnknown():
    knownList, unknownList = getUnAndKnownLists()

    knownList, unknownList = moveAToB(knownList, unknownList, knownPostsListbox.curselection())

    setUnAndKnownLists(unknownList, knownList)
    
def moveUnknownToKnown():
    knownList, unknownList = getUnAndKnownLists()

    unknownList, knownList = moveAToB(unknownList, knownList, unknownPostsListbox.curselection())

    setUnAndKnownLists(unknownList, knownList)
    

def moveAToB(a, b, aSelection):

    selectedIds = []
    for selectedIndex in aSelection:
        selectedIds.append(a[selectedIndex])
    for id in selectedIds:
        b.append(id)
        a.remove(id)

    a.sort()
    a.reverse()

    b.sort()
    b.reverse()
    
    return a, b
    
def getUnAndKnownLists():
    global knownPostsListVar, unknownPostsListVar
    knownList = []
    unknownList = []

    knownList = formatStrVarToList(knownPostsListVar)
    unknownList = formatStrVarToList(unknownPostsListVar)

    return knownList, unknownList

def setUnAndKnownLists(unknown, known):
    knownPostsListVar.set(known)
    unknownPostsListVar.set(unknown)

    updateDatabase()

    
def deleteUser():
    user = idEntryElement.get()
    service =  selectedService.get()
    if(databaseHelper.getUserData(user, service) == []):
        viewAddIdStatusLabel.config(bg="orange", text="Couldnt find user to delete")
    else:
        databaseHelper.deleteUserData(user, service)
        viewAddIdStatusLabel.config(bg="green", text="Deleted user")