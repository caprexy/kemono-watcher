from tkinter import *
from tkinter import ttk
from functions.operationHelper import passElements, addUser, getUpdates
from . import constants

root = None
inputFrame = None

selectedService = None

# operation options
options = constants.WEBSITES

def buildFrame():
    global selectedService, idEntryElement

    # first row
    frameRow = 1
    inputFrame.grid_columnconfigure(0, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(1, weight=1, uniform="equal")
    inputFrame.grid_columnconfigure(2, weight=1, uniform="equal")

    operationLabel = Label(inputFrame, text="Select service and user id:")
    operationLabel.grid(row=frameRow, column=0)
    selectedService = StringVar(root)
    selectedService.set(options[0])
    serviceSelectEle = OptionMenu( inputFrame , selectedService , *options )
    serviceSelectEle.grid( row=frameRow, column=1, pady= 10, sticky= W + E)
    serviceSelectEle.configure(width=10, height=2)

    idEntryElement = Entry(inputFrame)
    idEntryElement.grid(row=frameRow, column=2)

    # row 2
    frameRow = 2
    addButton = Button(inputFrame, text = "Add to subscriptions", command = addUser)
    addButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)
    addButton.configure(width=10, height=2)
    

    addUserResultEle = Label(inputFrame, text="")
    addUserResultEle.grid(row=frameRow, column=2)

    # row 3
    frameRow = 3
    seperator = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)
    
    # row 4
    frameRow = 4
    updateButton = Button(inputFrame, text = "Check subscription updates", command= getUpdates)
    updateButton.grid( row=frameRow, column=0, pady= 10, sticky= W + E)
    updateButton.configure(width=10, height=2)

    return idEntryElement, addUserResultEle, addButton


def initalizeInputFrame(rootIn):
    global inputFrame, root, selectedService
    root = rootIn
    
    inputFrame = Frame(root)
    inputFrame.grid_propagate(False)
    idEntryElement, addUserResultEle, addButton = buildFrame()

    passElements(idEntryElement, selectedService, addUserResultEle, addButton)
    return inputFrame
