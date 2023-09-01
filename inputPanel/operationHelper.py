from . import statusHelper
import threading
import tkinter
import webbrowser
import logging

idEntryElement = None
selectedService = None

addButton = None
knownPostsListVar = None
unknownPostsListVar = None

knownPostsListbox = None
unknownPostsListbox = None

knownUsersListVar = None
knownUsersListbox = None

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

def setDisplayUsers(knownUsersListVarIn, knownUsersListboxIn):
    global knownUsersListbox, knownUsersListVar
    
    knownUsersListVar = knownUsersListVarIn
    knownUsersListbox = knownUsersListboxIn
######


# actual operations
def addUser():
    global idEntryElement, selectedService, addButton
    addButton["state"] = "disabled"
    user = idEntryElement.get()
    service =  selectedService.get()
    
    logging.info("Trying to add a user")

    if(len(user) == 0):
        statusHelper.setuserOperationStatusValues("Missing Id!", "red")
        addButton["state"] = "normal"
        return
    elif not user.isnumeric():
        statusHelper.setuserOperationStatusValues("Non numeric id!", "red")
        addButton["state"] = "normal"
        return
    
    if(database.userExists(user, service)):
        statusHelper.setuserOperationStatusValues("User already exists!", "red")
        addButton["state"] = "normal"
    else:
        threading.Thread(target=database.createUser, args=(user, service, addButton, updateOperationPanel)).start()
    viewUserInfo()
    updateKnownListVar()

def updateOperationPanel():
    viewUserInfo()
    updateKnownListVar()

def clearOperationPanel():
    global idEntryElement, selectedService
    idEntryElement.delete(0, tkinter.END)
    knownPostsListVar.set([])
    unknownPostsListVar.set([])
    updateKnownListVar()
    

def viewUserInfo():
    global idEntryElement, selectedService, knownPostsListVar, unknownPostsListVar

    logging.info("Trying to view a user")
    
    userId = idEntryElement.get()
    service =  selectedService.get()

    userObj = database.getUserObj(userId, service)
    if(userObj == None):
        statusHelper.setuserOperationStatusValues("Couldnt find user!", "red")
        return
    
    logging.info("Got user "+ str(userObj))
    knownPostsListVar.set(userObj.checkedPostIds)
    unknownPostsListVar.set(userObj.uncheckedPostIds)
    
    statusHelper.setuserOperationStatusValues("Got user!", "green")


def deleteUser():
    user = idEntryElement.get()
    service =  selectedService.get()
    if(database.userExists(user, service) == []):
        statusHelper.setuserOperationStatusValues("Couldnt find user to delete", "orange")
    else:
        database.deleteUser(user, service, clearOperationPanel)

def getSelectedUsers():
    users = formatStrVarToList(knownUsersListVar)
    selectedVal = users[knownUsersListbox.curselection()[0]]

    service, selectedUser = selectedVal.split(":")

    selectedService.set(service)
    idEntryElement.delete(0, tkinter.END)
    idEntryElement.insert(0, selectedUser)
    viewUserInfo()

def updateKnownListVar():
    userList = database.getAllUserIdServices()
    knownUsers = []
    for user in userList:
        knownUsers.append(f"{user[1]}:{user[0]}")
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

    # error checking to ensure the total values are still the same
    newList = known + unknown
    newList.sort()

    if userObj.checkedPostIds == "": userObj.checkedPostIds = []
    if userObj.uncheckedPostIds == "": userObj.uncheckedPostIds = []

    oldList = userObj.checkedPostIds + userObj.uncheckedPostIds
    oldList.sort()

    if newList != oldList:
        logging.error("When trying to update the post lists, frontend != backend!")
        return

    userObj.checkedPostIds = known
    userObj.uncheckedPostIds = unknown

    database.updateUserObj(userObj)


    