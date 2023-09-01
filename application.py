from tkinter import *
from inputPanel import inputFrameHelper
from checkerPanel import outputFrameHelper
from models import databaseModel
import logging

#enable disable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# setup god window
root = Tk()

database = databaseModel.Database()

# setting up root geometry
root.geometry("1000x900")

# build main window which will be a panedwindow
mainWindow = PanedWindow(root, orient=HORIZONTAL)
mainWindow.pack(fill=BOTH, expand=TRUE)

# add said frames
mainWindow.add(inputFrameHelper.initalizeInputFrame(mainWindow, database), stretch="always")
mainWindow.add(outputFrameHelper.initalizeOutputFrame(mainWindow, database), stretch="always")



root.mainloop()