from tkinter import *
from tkinter import ttk
from . import inputController
import constants
from . import statusHelper

# frames operated in
parentFrame = None
inputFrame = None

# various widgets in need of saving
selectedServiceVar = None

knownPostsListVar = None
unknownPostsListVar = None

unknownPostsListbox = None
knownPostsListbox = None

idEntryElement = None
viewAddIdStatusLabel = None

# operation options
options = constants.SERVICES

def initalizeInputFrame(rootIn, database):
    global inputFrame, parentFrame
    parentFrame = rootIn
    
    inputFrame = Frame(rootIn)
    buildFrame()
    inputController.initalize(database)

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
    delete_userRow(frameRow)

    frameRow += 1
    seperatorRow(frameRow)

    frameRow += 1
    knownPostsRow(frameRow)

    frameRow += 1
    unknownPostsRow(frameRow)

    frameRow += 1
    seperatorRow(frameRow)
    
    frameRow += 1
    displayUsers(frameRow)


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
    idEntryElement.insert(0,"71308758")
    idEntryElement.grid(row=frameRow, column=2)

    inputController.set_service_and_user_id_ele(selectedServiceVar, idEntryElement)

def viewAddIdRow(frameRow):
    global viewAddIdStatusLabel
    addButton = Button(inputFrame, text = "Add id to subscriptions", command = inputController.add_user)
    addButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)
    addButton.configure(width=10, height=2)    

    userOperationStatusLabel = Label(inputFrame, text="")
    userOperationStatusLabel.grid(row=frameRow, column=2)
    statusHelper.setUserOperationStatusLabel(userOperationStatusLabel)
    inputController.set_add_button(addButton)

def delete_userRow(frameRow):
    delete_userButton = Button(inputFrame, text = "Delete user", command = inputController.delete_user, bg = "red")
    delete_userButton.grid( row = frameRow, column=0, pady= 10, sticky= W + E)
    delete_userButton.configure(width=10, height=2)

    openUserButton = Button(inputFrame, text = "Open user page", command = inputController.open_user_page)
    openUserButton.grid( row = frameRow, column=2, pady= 10, sticky= W + E)
    openUserButton.configure(width=10, height=2)

def seperatorRow(frameRow):
    seperator1 = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator1.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)

def knownPostsRow(frameRow):
    global  knownPostsListVar, unknownPostsListVar, unknownPostsListbox, knownPostsListbox
    knownPostsLabel = Label(inputFrame, text="Known posts")
    knownPostsLabel.grid(row=frameRow, column=0)

    knownPostsListVar = StringVar(value=[])
    knownPostsListbox = Listbox(inputFrame, selectmode= "extended", listvariable=knownPostsListVar)
    knownPostsListbox.grid( row=frameRow, column=1, pady= 10, sticky= "nsew")
    knownPostsListbox.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)

    move_from_known_to_unknownButton = Button(inputFrame, text = "Move known post to unknown", command= inputController.move_from_known_to_unknown)
    move_from_known_to_unknownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    move_from_known_to_unknownButton.configure(width=10, height=2)

    inputController.set_known_post_var_list(knownPostsListVar, knownPostsListbox)

def unknownPostsRow(frameRow):
    
    unknownPostLabels = Label(inputFrame, text="Unknown posts")
    unknownPostLabels.grid(row=frameRow, column=0)

    unknownPostsListVar = StringVar(value=[])
    unknownPostsListbox = Listbox(inputFrame, selectmode= "extended", listvariable=unknownPostsListVar)
    unknownPostsListbox.grid( row=frameRow, column=1, pady= 10,   sticky= "nsew")
    unknownPostsListbox.configure(width=10, height=2)
    inputFrame.grid_rowconfigure(frameRow, minsize=200)
    
    move_from_unknown_to_knownButton = Button(inputFrame, text = "Move unknown post to known", command= inputController.move_from_unknown_to_known)
    move_from_unknown_to_knownButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    move_from_unknown_to_knownButton.configure(width=10, height=2)

    inputController.set_unknown_post_var_list(unknownPostsListVar, unknownPostsListbox)


def displayUsers(frameRow):
    unknownPostLabels = Label(inputFrame, text="Known users")
    unknownPostLabels.grid(row=frameRow, column=0)

    knownUsersListVar = StringVar(value=[])
    knownUsersListbox = Listbox(inputFrame, selectmode= "single", listvariable=knownUsersListVar)
    knownUsersListbox.grid( row=frameRow, column=1, pady= 10,   sticky= "nsew")
    knownUsersListbox.configure(width=10, height=1)
    inputFrame.grid_rowconfigure(frameRow, minsize=100)

    getSelectedUserButton = Button(inputFrame, text = "Get selected user", command= inputController.get_selected_users)
    getSelectedUserButton.grid( row= frameRow, column=2, pady= 10, sticky= W + E)
    getSelectedUserButton.configure(width=10, height=2)

    inputController.set_display_users(knownUsersListVar, knownUsersListbox)