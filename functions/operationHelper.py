idEntryElement = None
selectedService = None
addUserResultEle = None

def passElements(idEntryElementIn, selectedServiceIn, addUserResultEleIn):
    global idEntryElement, selectedService, addUserResultEle
    selectedService = selectedServiceIn
    idEntryElement = idEntryElementIn
    addUserResultEle = addUserResultEleIn

def addUser():
    global idEntryElement, selectedService
    print(idEntryElement.get(), selectedService.get())

    if(len(idEntryElement.get()) == 0):
        addUserResultEle.config(text="Missing Id!", bg = "red")
    else:
        addUserResultEle.config(text="", bg = "#f0f0f0")


def getUpdates():
    print("a")