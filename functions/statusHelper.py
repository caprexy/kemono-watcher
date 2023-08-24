DEFAULT_BG_COLOR = "#f0f0f0"

memberOperationStatusLabel = None

def setMemberOperationStatusLabel(memberOperationStatusLabelIn):
    global memberOperationStatusLabel
    memberOperationStatusLabel = memberOperationStatusLabelIn

def setMemberOperationStatus(labelText, bgColor="default"):
    if(bgColor == "default"):
        memberOperationStatusLabel.config(text=labelText, bg = DEFAULT_BG_COLOR)
        return
    memberOperationStatusLabel.config(text=labelText, bg = bgColor)

def emptyMemberOperationStatus():
    memberOperationStatusLabel.config(text="", bg = DEFAULT_BG_COLOR)
