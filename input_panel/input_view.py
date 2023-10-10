""" Is the panel for most main user input"""
from tkinter import ttk, Frame, Label, StringVar, \
    OptionMenu, E,W, Entry, Button, HORIZONTAL, Listbox
import constants

from . import input_controller
from . import status_helper

# pylint: disable=C0103
# frames operated in
parent_frame = None
input_frame = None

# various widgets in need of saving
selected_service_var = None

id_entry_element = None
view_add_id_status_label = None

# operation options
options = constants.SERVICES
# pylint: enable=C0103

def initalize_input_frame(root_in, database):
    """Initalizes all globals and frames for the input frame

    Args:
        root_in (_type_): the parent tk panel that is the god tk panel
        database (_type_): the singular database created

    Returns:
        _type_: tk frame of the input
    """
    global input_frame, parent_frame
    parent_frame = root_in
    
    input_frame = Frame(root_in)
    build_frame()
    input_controller.initalize(database)

    return input_frame

def build_frame():
    """Builds the primary frame, 3 columns only
    """
    # frame config
    input_frame.grid_columnconfigure(0, weight=1, uniform="equal")
    input_frame.grid_columnconfigure(1, weight=1, uniform="equal")
    input_frame.grid_columnconfigure(2, weight=1, uniform="equal")
    input_frame.grid_propagate(False)

    frame_row = 1
    enter_service_and_id_row(frame_row)

    frame_row += 1
    view_add_id_row(frame_row)

    frame_row += 1
    delete_open_user_row(frame_row)

    frame_row += 1
    seperator_row(frame_row)

    frame_row += 1
    known_posts_row(frame_row)

    frame_row += 1
    unknown_posts_row(frame_row)

    frame_row += 1
    seperator_row(frame_row)
    
    frame_row += 1
    display_users(frame_row)


# functions to define the rows and the corresponding widgets
def enter_service_and_id_row(frame_row):
    """Row that has the list box for services and input box for id

    Args:
        frame_row (_type_): row number to exist on
    """
    global selected_service_var,  id_entry_element
    operation_label = Label(input_frame, text="Enter service and user id:")
    operation_label.grid(row=frame_row, column=0)
    selected_service_var = StringVar(parent_frame)
    selected_service_var.set(options[0])
    service_select_ele = OptionMenu( input_frame , selected_service_var , *options )
    service_select_ele.grid( row=frame_row, column=1, pady= 10, sticky= W + E)
    service_select_ele.configure(width=10, height=2)

    id_entry_element = Entry(input_frame)
    id_entry_element.insert(0,"71308758")
    id_entry_element.grid(row=frame_row, column=2)

    input_controller.set_service_and_user_id_ele(selected_service_var, id_entry_element)

def view_add_id_row(frame_row):
    """Makes the add id to subscriptions button row

    Args:
        frame_row (_type_): row number to exist on
    """
    add_button = Button(input_frame, text = "Add id to subscriptions", command = input_controller.add_user)
    add_button.grid( row = frame_row, column=1, pady= 10, sticky= W + E)
    add_button.configure(width=10, height=2)    

    user_operation_status_label = Label(input_frame, text="")
    user_operation_status_label.grid(row=frame_row, column=2)
    status_helper.set_user_operation_status_label(user_operation_status_label)
    input_controller.set_add_button(add_button)

def delete_open_user_row(frame_row):
    """Adds a delete user and open user page button

    Args:
        frame_row (_type_): row number to exist on
    """
    delete_user_button = Button(input_frame, text = "Delete user", command = input_controller.delete_user, bg = "red")
    delete_user_button.grid( row = frame_row, column=0, pady= 10, sticky= W + E)
    delete_user_button.configure(width=10, height=2)

    open_user_button = Button(input_frame, text = "Open user page", command = input_controller.open_user_page)
    open_user_button.grid( row = frame_row, column=2, pady= 10, sticky= W + E)
    open_user_button.configure(width=10, height=2)

def seperator_row(frame_row):
    """Row to create the seperator line

    Args:
        frame_row (_type_): row number to exist on
    """
    seperator1 = ttk.Separator(input_frame, orient=HORIZONTAL)
    seperator1.grid(row = frame_row, column=0, columnspan=3, sticky="ew", pady=10)

def known_posts_row(frame_row):
    """Creates a listbox for known posts and buttons to move known to unknown

    Args:
        frame_row (_type_): row number to exist on
    """
    known_posts_label = Label(input_frame, text="Known posts")
    known_posts_label.grid(row=frame_row, column=0)

    known_posts_list_var = StringVar(value=[])
    known_posts_listbox = Listbox(input_frame, selectmode= "extended", \
        listvariable=known_posts_list_var)
    known_posts_listbox.grid( row=frame_row, column=1, pady= 10, sticky= "nsew")
    known_posts_listbox.configure(width=10, height=2)
    input_frame.grid_rowconfigure(frame_row, minsize=200)

    move_from_known_to_unknown_button = Button(input_frame, \
        text = "Move known post to unknown", \
        command= input_controller.move_from_known_to_unknown)
    move_from_known_to_unknown_button.grid( row= frame_row, column=2, pady= 10, sticky= W + E)
    move_from_known_to_unknown_button.configure(width=10, height=2)

    input_controller.set_known_post_var_list(known_posts_list_var, known_posts_listbox)

def unknown_posts_row(frame_row):
    """Creates a listbox for unknown posts and buttons to move unknown to known

    Args:
        frame_row (_type_): row number to exist on
    """
    
    unknown_post_labels = Label(input_frame, text="Unknown posts")
    unknown_post_labels.grid(row=frame_row, column=0)

    unknown_posts_list_var = StringVar(value=[])
    unknown_posts_listbox = Listbox(input_frame, selectmode= "extended", \
        listvariable=unknown_posts_list_var)
    unknown_posts_listbox.grid( row=frame_row, column=1, pady= 10,   sticky= "nsew")
    unknown_posts_listbox.configure(width=10, height=2)
    input_frame.grid_rowconfigure(frame_row, minsize=200)
    
    move_from_unknown_to_known_button = Button(input_frame, \
        text = "Move unknown post to known", \
        command= input_controller.move_from_unknown_to_known)
    move_from_unknown_to_known_button.grid( row= frame_row, column=2, pady= 10, sticky= W + E)
    move_from_unknown_to_known_button.configure(width=10, height=2)

    input_controller.set_unknown_post_var_list(unknown_posts_list_var, unknown_posts_listbox)


def display_users(frame_row):
    """Creates a listbox for known users and a button to open that user

    Args:
        frame_row (_type_):  row number to exist on
    """
    unknown_post_labels = Label(input_frame, text="Known users")
    unknown_post_labels.grid(row=frame_row, column=0)

    known_users_list_var = StringVar(value=[])
    known_users_listbox = Listbox(input_frame, selectmode= "single", \
        listvariable=known_users_list_var)
    known_users_listbox.grid( row=frame_row, column=1, pady= 10,   sticky= "nsew")
    known_users_listbox.configure(width=10, height=1)
    input_frame.grid_rowconfigure(frame_row, minsize=100)

    get_selected_user_button = Button(input_frame, text = "Get selected user", \
        command= input_controller.get_selected_users)
    get_selected_user_button.grid( row= frame_row, column=2, pady= 10, sticky= W + E)
    get_selected_user_button.configure(width=10, height=2)

    input_controller.set_display_users(known_users_list_var, known_users_listbox)
