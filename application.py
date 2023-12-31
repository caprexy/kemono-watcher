"Main file to run application"

from tkinter import Tk, PanedWindow, HORIZONTAL, BOTH, TRUE
import logging

from input_panel import input_view
from output_panel import output_view
from models import database_model

#enable disable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# setup god window
root = Tk()

database = database_model.Database()

# setting up root geometry
root.geometry("1000x900")

# build main window which will be a panedwindow
mainWindow = PanedWindow(root, orient=HORIZONTAL)
mainWindow.pack(fill=BOTH, expand=TRUE)

# add said frames
mainWindow.add(input_view.initalize_input_frame(mainWindow, database), stretch="always")
mainWindow.add(output_view.initalize_output_frame(mainWindow, database), stretch="always")

root.mainloop()
