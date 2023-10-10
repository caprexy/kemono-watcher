"""Contains all the frontend elements to be displayed to the user"""
from tkinter import StringVar, Listbox, Button, Label, W, E, Frame
import webbrowser

from inputPanel import status_helper
from . import output_controller

# frame information
# pylint: disable=C0103
root = None
output_frame = None
list_known_posts = None 
new_posts_list_var = None
database = None
# pylint: enable=C0103

def build_frame():
    """ Primary frame for the output view as a whole. 
        The output view is where users can see the output of checks for unseen new links and unchecked links

    Returns:
        _type_: _description_
    """
    global list_known_posts, new_posts_list_var

    # limit to 3 columns
    output_frame.grid_columnconfigure(0, weight=1, uniform="equal")
    output_frame.grid_columnconfigure(1, weight=1, uniform="equal")
    output_frame.grid_columnconfigure(2, weight=1, uniform="equal")

    frame_row = 1
    update_posts_button = Button(output_frame, 
                text = "Update unread posts", command = output_controller.get_unread_posts)
    update_posts_button.grid( row = frame_row, column=1, pady= 10, sticky= W + E)

    get_update_status = Label(output_frame, text="No updates gotten", bg = "Grey", wraplength=100)
    get_update_status.grid(row=frame_row, column=0)
    status_helper.set_get_updates_status_label(get_update_status)

    frame_row += 1
    new_posts_list_var = StringVar(value=[])
    list_known_posts = Listbox(output_frame, selectmode= "extended", listvariable=new_posts_list_var)
    list_known_posts.grid( row=frame_row, column=1, pady= 10, sticky= "nsew")
    list_known_posts.configure(width=10, height=2)
    output_frame.grid_rowconfigure(frame_row, minsize=200)

    frame_row += 1
    open_selected_button = Button(output_frame, text = "Open selected posts", command = open_selected_ids)
    open_selected_button.grid( row = frame_row, column=0, pady= 10, sticky= W + E)

    finish_posts_button = Button(output_frame, text = "Finish selected posts", command = know_unknown_post)
    finish_posts_button.grid( row = frame_row, column=2, pady= 10, sticky= W + E)

    return new_posts_list_var, update_posts_button


    
def initalize_output_frame(root_in, database_in):
    """Called to setup the view by the main application

    Args:
        root_in (_type_): root frame by the main application
        database_in (_type_): main database by the main application

    Returns:
        _type_: returns the frame created for this output view
    """
    global root,output_frame, database, new_posts_list_var
    root = root_in
    database = database_in

    output_frame = Frame(root, bg="grey")
    output_frame.grid_propagate(False)

    new_posts_list_var, update_posts_button = build_frame()
    output_controller.pass_vars(new_posts_list_var, update_posts_button, database)

    return output_frame

## maybe move to controller but might require more variable passing
def open_selected_ids():
    """Minor function to open selected posts"""
    for selection in list_known_posts.curselection():
        post_id, service, user_id = list_known_posts.get(selection).split(",")
        webbrowser.open("https://kemono.party/"+service.lower()+"/user/"+user_id+"/post/"+post_id)

def know_unknown_post():
    """Minor function to know an unknown post"""
    for selection in list_known_posts.curselection():
        post_id, service, user_id = list_known_posts.get(selection).split(",")
        database.know_unknown_post(user_id, service, post_id)
    
    offset = 0
    for selection in list_known_posts.curselection():
        list_known_posts.delete(selection-offset)
        offset += 1
    