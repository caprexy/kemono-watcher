from tkinter import *
from PIL import ImageTk, Image
from functions.inputFrameHelper import *
from functions.outputFrameHelper import *



# setup god window
root = Tk()

# setting up root geometry
root.geometry("1000x900")

# build main window which will be a panedwindow
mainWindow = PanedWindow(root, orient=HORIZONTAL)
mainWindow.pack(fill=BOTH, expand=TRUE)

# add said frames
mainWindow.add(initalizeInputFrame(mainWindow), stretch="always")
mainWindow.add(initalizeOutputFrame(mainWindow), stretch="always")



root.mainloop()