
from . import databaseModel
from . import statusHelper
import re
import threading
import tkinter
import webbrowser

idEntryElement = None
selectedService = None

addButton = None
knownPostsListVar = None
unknownPostsListVar = None

knownPostsListbox = None
unknownPostsListbox = None

knownUsersListVar = None

unknownPostsListbox = None

database = None
def initalize(databaseIn):
    global database
    database = databaseIn

    updateKnownListVar()

######
## set needed elements from the frame
def setServiceAndUserId(selectedServiceVar, userIdEle):
    global idEntryElement, selectedService
    selectedService = selectedServiceVar
    idEntryElement = userIdEle

def setAddButton(addButtonIn):
    global addButton
    addButton = addButtonIn

def setKnownPostVarList(knownPostsListVarIn, knownPostsListboxIn):
    global knownPostsListVar, knownPostsListbox

    knownPostsListVar = knownPostsListVarIn
    knownPostsListbox = knownPostsListboxIn

def setUnknownPostVarList(unknownPostsListVarIn, unknownPostsListboxIn):
    global unknownPostsListVar, unknownPostsListbox
    
    unknownPostsListVar = unknownPostsListVarIn
    unknownPostsListbox = unknownPostsListboxIn

def setDisplayUsers(knownUsersListVarIn, unknownPostsListboxIn):
    global unknownPostsListbox, knownUsersListVar
    
    knownUsersListVar = knownUsersListVarIn
    unknownPostsListbox = unknownPostsListboxIn
######


# actual operations
def addUser():
    global idEntryElement, selectedService, addButton
    addButton["state"] = "disabled"
    user = idEntryElement.get()
    service =  selectedService.get()
    
    if(len(user) == 0):
        statusHelper.setMemberOperationStatus("Missing Id!", "red")
        addButton["state"] = "normal"
    elif(database.userExists(user, service)):
        statusHelper.setMemberOperationStatus("User already exists!", "red")
        addButton["state"] = "normal"
    else:
        threading.Thread(target=database.createUser, args=(user, service, addButton)).start()
    updateKnownListVar()
    viewUserInfo()

def viewUserInfo():
    global idEntryElement, selectedService, knownPostsListVar, unknownPostsListVar

    userId = idEntryElement.get()
    service =  selectedService.get()

    userObj = database.getUserObj(userId, service)
    if(userObj == None):
        statusHelper.setMemberOperationStatus(text="User couldnt find user!", bg = "red")
        return
    
    knownPostsListVar.set(userObj.checkedPostIds)
    unknownPostsListVar.set(userObj.uncheckedPostIds)
    
    statusHelper.setMemberOperationStatus("Got user!", "green")


def deleteUser():
    user = idEntryElement.get()
    service =  selectedService.get()
    if(databaseHelper.getUserData(user, service) == []):
        statusHelper.setMemberOperationStatus(bg="orange", text="Couldnt find user to delete")
    else:
        databaseHelper.deleteUserData(user, service)
        statusHelper.setMemberOperationStatus(bg="green", text="Deleted user")

def getSelectedUsers():
    users = formatStrVarToList(knownUsersListVar)
    selectedVal = users[unknownPostsListbox.curselection()[0]]

    service, selectedUser = selectedVal.split(":")

    selectedService.set(service)
    idEntryElement.delete(0, tkinter.END)
    idEntryElement.insert(0, selectedUser)
    viewUserInfo()

def updateKnownListVar():
    userList = database.getAllUserObjs()
    knownUsers = []
    for user in userList:
        knownUsers.append(f"{user.service}:{user.id}")
    knownUsersListVar.set(knownUsers)

def openUserPage():
    global idEntryElement, selectedService
    user = idEntryElement.get()
    service =  selectedService.get()
    webbrowser.open("https://kemono.party/"+service.lower()+"/user/"+user)

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

    # updating the database and userobj
    userId = idEntryElement.get()
    service =  selectedService.get()

    userObj = database.getUserObj(userId, service)

    userObj.checkedPostIds = known
    userObj.uncheckedPostIds = unknown

    database.writeDatabase()


    