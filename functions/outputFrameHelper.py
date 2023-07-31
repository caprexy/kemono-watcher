from tkinter import *

# frame information
root = None
outputFrame = None

def initalizeOutputFrame(rootIn):
    global outputFrame, root
    root = rootIn

    outputFrame = Frame(root, bg="red")
    return outputFrame