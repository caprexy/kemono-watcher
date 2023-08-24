from tkinter import *
from functions.inputFrameHelper import *
from functions.outputFrameHelper import *
import functions.databaseModel


# setup god window
root = Tk()

database = functions.databaseModel.initalizeDatabase()

# setting up root geometry
root.geometry("1000x900")

# build main window which will be a panedwindow
mainWindow = PanedWindow(root, orient=HORIZONTAL)
mainWindow.pack(fill=BOTH, expand=TRUE)

# add said frames
mainWindow.add(initalizeInputFrame(mainWindow, database), stretch="always")
mainWindow.add(initalizeOutputFrame(mainWindow, database), stretch="always")



root.mainloop()