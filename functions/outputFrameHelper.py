from tkinter import *
from . import kemonoHelper

from . import databaseModel
import webbrowser

# frame information
root = None
outputFrame = None
getUpdateStatus = None
listKnownPosts = None
newPostsListVar = None
database = None

def buildFrame():
    global root,outputFrame, listKnownPosts, newPostsListVar

    outputFrame.grid_columnconfigure(0, weight=1, uniform="equal")
    outputFrame.grid_columnconfigure(1, weight=1, uniform="equal")
    outputFrame.grid_columnconfigure(2, weight=1, uniform="equal")

    frameRow = 1
    updatePostsButton = Button(outputFrame, text = "Update unread posts", command = kemonoHelper.getUnreadPosts)
    updatePostsButton.grid( row = frameRow, column=1, pady= 10, sticky= W + E)

    getUpdateStatus = Label(outputFrame, text="No updates gotten", bg = "Grey", wraplength=100)
    getUpdateStatus.grid(row=frameRow, column=0)

    frameRow += 1
    newPostsListVar = StringVar(value=[])
    listKnownPosts = Listbox(outputFrame, selectmode= "extended", listvariable=newPostsListVar)
    listKnownPosts.grid( row=frameRow, column=1, pady= 10, sticky= "nsew")
    listKnownPosts.configure(width=10, height=2)
    outputFrame.grid_rowconfigure(frameRow, minsize=200)

    frameRow += 1
    openSelectedButton = Button(outputFrame, text = "Open selected posts", command = openSelectedIds)
    openSelectedButton.grid( row = frameRow, column=0, pady= 10, sticky= W + E)

    finishPostsButton = Button(outputFrame, text = "Finish selected posts", command = knowUnknownPost)
    finishPostsButton.grid( row = frameRow, column=2, pady= 10, sticky= W + E)

    return newPostsListVar, getUpdateStatus, updatePostsButton


    
def initalizeOutputFrame(rootIn, databaseIn):
    global root,outputFrame, database
    root = rootIn
    database = databaseIn

    outputFrame = Frame(root, bg="grey")
    outputFrame.grid_propagate(False)

    newPostsListVar, getUpdateStatus, updatePostsButton = buildFrame()
    kemonoHelper.passVars(newPostsListVar, getUpdateStatus, updatePostsButton, database)

    return outputFrame

def openSelectedIds():
    global listKnownPosts
    for selection in listKnownPosts.curselection():
        userId, service, postId = listKnownPosts.get(selection).split(",")
        webbrowser.open("https://kemono.party/"+service.lower()+"/user/"+userId+"/post/"+postId)

def knowUnknownPost():
    global listKnownPosts
    for selection in listKnownPosts.curselection():
        userId, service, postId = listKnownPosts.get(selection).split(",")
        database.knowUnknownPost(userId, service, postId)
    
    offset = 0
    for selection in listKnownPosts.curselection():
        listKnownPosts.delete(selection-offset)
        offset += 1
    