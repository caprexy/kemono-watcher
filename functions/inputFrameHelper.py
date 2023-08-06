from tkinter import *
from tkinter import ttk
from . import operationHelper
from . import databaseHelper
from . import constants

# frames operated in
parentFrame = None
inputFrame = None

# various widgets in need of saving
selectedServiceVar = None

knownPostsListVar = None
unknownPostsListVar = None

listUnknownPosts = None
listKnownPosts = None

idEntryElement = None
viewAddIdStatusLabel = None

# operation options
options = constants.WEBSITES

def initalizeInputFrame(rootIn):
    global inputFrame, parentFrame
    parentFrame = rootIn
    
    inputFrame = Frame(rootIn)
    buildFrame()

    return inputFrame

def buildFrame():
    # frame config
    inputFrame.grid_columnconfigure(0, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(1, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(2, weight=1, uniform="equal")
    inputFrame.grid_propagate(False)

    frameRow = 1
    enterServiceAndIdRow(frameRow)

    frameRow += 1
    viewAddIdRow(frameRow)

    frameRow += 1
    seperatorRow(frameRow)

    frameRow += 1
    knownPostsRow(frameRow)

    frameRow += 1
    unknownPostsRow(frameRow)

    frameRow += 1
    seperatorRow(frameRow)

    frameRow += 1
    deleteUserRow(frameRow)

# functions to define the rows and the corresponding widgets
def enterServiceAndIdRow(frameRow):
    global selectedServiceVar,  idEntryElement
    operationLabel = Label(inputFrame, text="Enter service and user id:")
    operationLabel.grid(row=frameRow, column=0)
    selectedServiceVar = StringVar(parentFrame)
    selectedServiceVar.set(options[0])
    serviceSelectEle = OptionMenu( inputFrame , selectedServiceVar , *options )
    serviceSelectEle.grid( row=frameRow, column=1, pady= 10, sticky= W + E)
    serviceSelectEle.configure(width=10, height=2)

    idEntryElement = Entry(inputFrame)
    idEntryElement.grid(row=frameRow, column=2)

    operationHelper.setServiceAndUserId(selectedServiceVar, idEntryElement)
    idEntryElement.insert(0,"6185029")

def viewAddIdRow(frameRow):
    global viewAddIdStatusLabel
    viewButton = Button(inputFrame, text = "View id info", command = operationHelper.viewUserInfo)
    viewButton.grid( row = frameRow, column=0, pady= 10, sticky= W + E)
    viewButton.configure(width=10, height=2)

    addButton = Button(inputFrame, text = "Add id to subscriptions", command = operationHelper.addUser)
    addButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)
    addButton.configure(width=10, height=2)
    

    viewAddIdStatusLabel = Label(inputFrame, text="")
    viewAddIdStatusLabel.grid(row=frameRow, column=2)
    operationHelper.setViewAddIdStatusLabel(viewAddIdStatusLabel)
    operationHelper.setAddButton(addButton)

def seperatorRow(frameRow):
    seperator1 = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator1.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)

def knownPostsRow(frameRow):
    global  knownPostsListVar, unknownPostsListVar, listUnknownPosts, listKnownPosts
    knownPostsLabel = Label(inputFrame, text="Known posts")
    knownPostsLabel.grid(row=frameRow, column=0)

    knownPostsListVar = StringVar(value=[])
    listKnownPosts = Listbox(inputFrame, selectmode= "extended", listvariable=knownPostsListVar)
    listKnownPosts.grid( row=frameRow, column=1, pady= 10, sticky= "nsew")
    listKnownPosts.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)

    moveKnownToUnknownButton = Button(inputFrame, text = "Move known post to unknown", command= moveKnownToUnknown)
    moveKnownToUnknownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    moveKnownToUnknownButton.configure(width=10, height=2)

    operationHelper.setKnownPostVar(knownPostsListVar)

def unknownPostsRow(frameRow):
    
    unknownPostLabels = Label(inputFrame, text="Unknown posts")
    unknownPostLabels.grid(row=frameRow, column=0)

    unknownPostsListVar = StringVar(value=[])
    listUnknownPosts = Listbox(inputFrame, selectmode= "extended", listvariable=unknownPostsListVar)
    listUnknownPosts.grid( row=frameRow, column=1, pady= 10,   sticky= "nsew")
    listUnknownPosts.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)
    
    moveUnknownToKnownButton = Button(inputFrame, text = "Move unknown post to known", command= moveUnknownToKnown)
    moveUnknownToKnownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    moveUnknownToKnownButton.configure(width=10, height=2)

    operationHelper.setUnknownPostVar(unknownPostsListVar)

def deleteUserRow(frameRow):
    deleteUserButton = Button(inputFrame, text = "Delete user", command = deleteUser)
    deleteUserButton.grid( row = frameRow, column=0, pady= 10, sticky= W + E)
    deleteUserButton.configure(width=10, height=2)




def moveKnownToUnknown():
    global listKnownPosts
    knownList, unknownList = getUnAndKnownLists()

    knownList, unknownList = moveAToB(knownList, unknownList, listKnownPosts.curselection())

    setUnAndKnownLists(unknownList, knownList)
    
def moveUnknownToKnown():
    global listUnknownPosts
    knownList, unknownList = getUnAndKnownLists()

    unknownList, knownList = moveAToB(unknownList, knownList, listUnknownPosts.curselection())

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

    knownList = operationHelper.formatStrVarToList(knownPostsListVar)
    unknownList = operationHelper.formatStrVarToList(unknownPostsListVar)

    return knownList, unknownList

def setUnAndKnownLists(unknown, known):
    knownPostsListVar.set(known)
    unknownPostsListVar.set(unknown)

    operationHelper.updateDatabase()

    
def deleteUser():
    user = idEntryElement.get()
    service =  selectedServiceVar.get()
    if(databaseHelper.getUserData(user, service) == []):
        viewAddIdStatusLabel.config(bg="orange", text="Couldnt find user to delete")
    else:
        databaseHelper.deleteUserData(user, service)
        viewAddIdStatusLabel.config(bg="green", text="Deleted user")