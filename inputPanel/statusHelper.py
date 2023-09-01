DEFAULT_BG_COLOR = "#f0f0f0"

userOperationStatusLabel = None

def setUserOperationStatusLabel(userOperationStatusLabelIn):
    global userOperationStatusLabel
    userOperationStatusLabel = userOperationStatusLabelIn

def setuserOperationStatusValues(labelText, bgColor="default"):
    if(bgColor == "default"):
        userOperationStatusLabel.config(text=labelText, bg = DEFAULT_BG_COLOR)
        return
    userOperationStatusLabel.config(text=labelText, bg = bgColor)

def clearUserOperationStatus():
    userOperationStatusLabel.config(text="", bg = DEFAULT_BG_COLOR)


getUpdatesStatusLabel = None

def setGetUpdatesStatusLabel(getUpdatesStatusLabelIn):
    global getUpdatesStatusLabel
    getUpdatesStatusLabel = getUpdatesStatusLabelIn


def setGetUpdatesStatusLabelValues(labelText, bgColor="default"):
    if(bgColor == "default"):
        getUpdatesStatusLabel.config(text=labelText, bg = DEFAULT_BG_COLOR)
        return
    getUpdatesStatusLabel.config(text=labelText, bg = bgColor)

def clearGetUpdatesStatusLabel():
    getUpdatesStatusLabel.config(text="", bg = DEFAULT_BG_COLOR)