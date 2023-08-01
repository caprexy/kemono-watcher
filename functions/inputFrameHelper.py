from tkinter import *
from tkinter import ttk
from . import operationHelper
from . import constants

root = None
inputFrame = None

selectedService = None

knownPostsListVar = None
unknownPostsListVar = None
listUnknownPosts = None
listKnownPosts = None

# operation options
options = constants.WEBSITES

def buildFrame():
    global selectedService, idEntryElement, knownPostsListVar, unknownPostsListVar, listUnknownPosts, listKnownPosts

    # first row
    frameRow = 1
    inputFrame.grid_columnconfigure(0, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(1, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(2, weight=1, uniform="equal")

    operationLabel = Label(inputFrame, text="Enter service and user id:")
    operationLabel.grid(row=frameRow, column=0)
    selectedService = StringVar(root)
    selectedService.set(options[0])
    serviceSelectEle = OptionMenu( inputFrame , selectedService , *options )
    serviceSelectEle.grid( row=frameRow, column=1, pady= 10, sticky= W + E)
    serviceSelectEle.configure(width=10, height=2)

    idEntryElement = Entry(inputFrame)
    idEntryElement.grid(row=frameRow, column=2)

    idEntryElement.insert(0,"6185029")

    # row 2
    frameRow += 1
    viewButton = Button(inputFrame, text = "View id info", command = operationHelper.viewUserInfo)
    viewButton.grid( row = frameRow, column=0, pady= 10, sticky= W + E)
    viewButton.configure(width=10, height=2)

    addButton = Button(inputFrame, text = "Add to subscriptions", command = operationHelper.addUser)
    addButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)
    addButton.configure(width=10, height=2)
    

    addUserResultEle = Label(inputFrame, text="")
    addUserResultEle.grid(row=frameRow, column=2)

    # row 3
    frameRow += 1
    seperator1 = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator1.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)
    
    # row 4
    frameRow += 1
    updateButton = Button(inputFrame, text = "Check subscription updates", command= operationHelper.getUpdates)
    updateButton.grid( row= frameRow, column=1, pady= 10, sticky= W + E)
    updateButton.configure(width=10, height=2)

    ###########
    frameRow += 1
    seperator2 = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator2.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)

    ###########
    frameRow += 1
    addUserResultEle = Label(inputFrame, text="Known posts")
    addUserResultEle.grid(row=frameRow, column=0)

    knownPostsListVar = StringVar(value=[])
    listKnownPosts = Listbox(inputFrame, selectmode= "extended", listvariable=knownPostsListVar)
    listKnownPosts.grid( row=frameRow, column=1, pady= 10, sticky= "nsew")
    listKnownPosts.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)

    moveKnownToUnknownButton = Button(inputFrame, text = "Move highlighted known post to unknown", command= moveKnownToUnknown)
    moveKnownToUnknownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    moveKnownToUnknownButton.configure(width=10, height=2)

    ###########
    frameRow += 1
    addUserResultEle = Label(inputFrame, text="Unknown posts")
    addUserResultEle.grid(row=frameRow, column=0)

    unknownPostsListVar = StringVar(value=[])
    addUserResultEle = Label(inputFrame, text="")
    addUserResultEle.grid(row=frameRow, column=2)

    listUnknownPosts = Listbox(inputFrame, selectmode= "extended", listvariable=unknownPostsListVar)
    listUnknownPosts.grid( row=frameRow, column=1, pady= 10,   sticky= "nsew")
    listUnknownPosts.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)
    
    moveUnknownToKnownButton = Button(inputFrame, text = "Move highlighted unknown post to known", command= moveUnknownToKnown)
    moveUnknownToKnownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    moveUnknownToKnownButton.configure(width=10, height=2)

    return idEntryElement, addUserResultEle, addButton, 

def initalizeInputFrame(rootIn):
    global inputFrame, root, selectedService, knownPostsListVar, unknownPostsListVar
    root = rootIn
    
    inputFrame = Frame(root)
    inputFrame.grid_propagate(False)
    idEntryElement, addUserResultEle, addButton = buildFrame()

    operationHelper.passElements(idEntryElement, selectedService, addUserResultEle, addButton, knownPostsListVar, unknownPostsListVar)
    return inputFrame

def moveKnownToUnknown():
    global knownPostsListVar, unknownPostsListVar, listKnownPosts
    knownList = []
    unknownList = []

    if(len( knownPostsListVar.get()) != 0):
        knownList = knownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(knownList[-1] == ''): knownList.pop()
    if(len( unknownPostsListVar.get()) != 0):
        unknownList = unknownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(unknownList[-1] == ''): unknownList.pop()

    for selectedIndex in listKnownPosts.curselection():
        unknownList.append(knownList[selectedIndex])
        knownList.pop(selectedIndex)
    unknownList.sort()
    unknownList.reverse()

    knownPostsListVar.set(knownList)
    unknownPostsListVar.set(unknownList)

    operationHelper.updateDatabase()
    
def moveUnknownToKnown():
    global knownPostsListVar, unknownPostsListVar, listUnknownPosts
    knownList = []
    unknownList = []

    if(len( knownPostsListVar.get()) != 0):
        knownList = knownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(knownList[-1] == ''): knownList.pop()
    if(len( unknownPostsListVar.get()) != 0):
        unknownList = unknownPostsListVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if(unknownList[-1] == ''): unknownList.pop()

    for selectedIndex in listUnknownPosts.curselection():
        knownList.append(unknownList[selectedIndex])
        unknownList.pop(selectedIndex)
    knownList.sort()
    knownList.reverse()

    knownPostsListVar.set(knownList)
    unknownPostsListVar.set(unknownList)
    
    operationHelper.updateDatabase()
    