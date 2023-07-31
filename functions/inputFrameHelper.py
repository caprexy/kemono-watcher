from tkinter import *
from tkinter import ttk
from functions.operationHelper import passElements, addUser, getUpdates


root = None
inputFrame = None

selectedService = None

# operation options
options = [
    "Patreon",
    "Pixiv Fanbox",
    "Discord",
    "Fantia"
]

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
    loadButton = Button(inputFrame, text = "Add to subscriptions", command = addUser)
    loadButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)
    loadButton.configure(width=10, height=2)
    

    addUserResultEle = Label(inputFrame, text="")
    addUserResultEle.grid(row=frameRow, column=2)

    # row 3
    frameRow = 3
    seperator = ttk.Separator(inputFrame, orient=HORIZONTAL)
    seperator.grid(row = frameRow, column=0, columnspan=3, sticky="ew", pady=10)
    
    # row 4
    frameRow = 4
    loadButton = Button(inputFrame, text = "Check subscription updates", command= getUpdates)
    loadButton.grid( row=frameRow, column=0, pady= 10, sticky= W + E)
    loadButton.configure(width=10, height=2)

    return idEntryElement, addUserResultEle


def initalizeInputFrame(rootIn):
    global inputFrame, root, selectedService
    root = rootIn
    
    inputFrame = Frame(root)
    inputFrame.grid_propagate(False)
    idEntryElement, addUserResultEle = buildFrame()

    passElements(idEntryElement, selectedService, addUserResultEle)
    return inputFrame
