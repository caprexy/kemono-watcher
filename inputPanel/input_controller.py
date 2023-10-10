""" All functions needed for the view, and calls the database to modify it """
import threading
import tkinter
import webbrowser
import logging

from models.databaseModel import Database
from . import statusHelper

# pylint: disable=C0103
id_entry_ele = None
selected_service = None

add_button = None
known_posts_list_var = None
unknown_posts_list_var = None

known_posts_list_box = None
unknown_posts_list_box = None

known_user_list_var = None
known_user_list_box = None

database = None
# pylint: enable=C0103

def initalize(database_in: Database):
    """Called to setup database to be used by the controller and anything else necessary
    Args:
        database_in (Database): _description_
    """
    global database
    database = database_in

    update_known_list()

######
## set needed elements from the frame
# pylint: disable=C0116
def set_service_and_user_id_ele(selected_service_var, user_id_ele):
    global id_entry_ele, selected_service
    selected_service = selected_service_var
    id_entry_ele = user_id_ele

def set_add_button(add_button_in):
    global add_button
    add_button = add_button_in

def set_known_post_var_list(known_posts_list_var_in, known_posts_list_box_in):
    global known_posts_list_var, known_posts_list_box

    known_posts_list_var = known_posts_list_var_in
    known_posts_list_box = known_posts_list_box_in

def set_unknown_post_var_list(unknown_posts_list_var_in, unknown_posts_list_box_in):
    global unknown_posts_list_var, unknown_posts_list_box
    
    unknown_posts_list_var = unknown_posts_list_var_in
    unknown_posts_list_box = unknown_posts_list_box_in

def set_display_users(known_user_list_var_in, known_user_list_box_in):
    global known_user_list_box, known_user_list_var
    
    known_user_list_var = known_user_list_var_in
    known_user_list_box = known_user_list_box_in
# pylint: enable=C0116
######


# actual operations
def add_user():
    """Adds a user and handles all UI changes required to do so
    """
    global add_button
    add_button["state"] = "disabled"
    user = id_entry_ele.get()
    service =  selected_service.get()
    
    logging.info("Trying to add a user")

    if len(user) == 0:
        statusHelper.setuserOperationStatusValues("Missing Id!", "red")
        add_button["state"] = "normal"
        return
    elif not user.isnumeric():
        statusHelper.setuserOperationStatusValues("Non numeric id!", "red")
        add_button["state"] = "normal"
        return
    
    if database.does_user_exist(user, service):
        statusHelper.setuserOperationStatusValues("User already exists!", "red")
        add_button["state"] = "normal"
    else:
        threading.Thread(target=database.create_user, args=(user, service, add_button, update_operation_panel)).start()
    view_user_info()
    update_known_list()

def update_operation_panel():
    """Central function to be called when UI eles on input panel needs to be updated and not done in function
    (ex: status change)
    """
    view_user_info()
    update_known_list()

def clear_operation_panel():
    """Clears out any information in the input panel
    """
    id_entry_ele.delete(0, tkinter.END)
    known_posts_list_var.set([])
    unknown_posts_list_var.set([])
    update_known_list()
    

def view_user_info():
    """Tries to view a user and set all according input panel elements
    """

    logging.info("Trying to view a user")
    
    user_id = id_entry_ele.get()
    service =  selected_service.get()

    user_obj = database.get_user_obj(user_id, service)
    if user_obj is None:
        statusHelper.setuserOperationStatusValues("Couldnt find user!", "red")
        return
    
    logging.info("Got user %s", str(user_obj))
    known_posts_list_var.set(user_obj.checked_post_ids)
    unknown_posts_list_var.set(user_obj.unchecked_post_ids)
    
    statusHelper.setuserOperationStatusValues("Got user!", "green")


def delete_user():
    """Called when deleting a user, starts the deletion call and updates UI elements
    """
    user = id_entry_ele.get()
    service =  selected_service.get()
    if database.does_user_exist(user, service) == []:
        statusHelper.setuserOperationStatusValues("Couldnt find user to delete", "orange")
    else:
        database.delete_user(user, service, clear_operation_panel)

def get_selected_users():
    """Called when trying to open a user and updates corresponding UI elements
    """
    if known_user_list_box.curselection() is ():
        return
    
    users = format_strvar_to_strlist(known_user_list_var)
    
    selectedVal = users[known_user_list_box.curselection()[0]]

    service, selectedUser = selectedVal.split(":")

    selected_service.set(service)
    id_entry_ele.delete(0, tkinter.END)
    id_entry_ele.insert(0, selectedUser)
    view_user_info()

def update_known_list():
    """Called to update the known users UI element
    """
    user_list = database.get_all_user_id_and_services() # PLEASE REWRITE TO NOT CALL THE DATABASE
    known_users = []
    for user in user_list:
        known_users.append(f"{user[1]}:{user[0]}")
    known_user_list_var.set(known_users)

def open_user_page():
    """Called to open the current user in website form
    """
    user = id_entry_ele.get()
    service =  selected_service.get()
    if not database.does_user_exist(user, service):
        return
    webbrowser.open("https://kemono.party/"+service.lower()+"/user/"+user)

def format_strvar_to_strlist(strVar)->list[str]:
    """Utility function to handle the stringVar from tk and convert into list

    Args:
        strVar (_type_): tk's stringvar

    Returns:
        list[str]: list of str
    """
    new_list = []
    if len( strVar.get()) != 0:
        new_list = strVar.get()[1:-1].replace('\'','').replace(' ','').split(",")
        if new_list[-1] == '': 
            new_list.pop()
    return new_list


def move_from_known_to_unknown():
    """Takes the selected value in the known and unknown listbox and moves it between lists
    """
    known_list, unknown_list = get_known_and_unknown_lists()

    known_list, unknown_list = move_from_a_to_b(known_list, unknown_list, known_posts_list_box.curselection())

    set_known_and_unknown_lists(unknown_list, known_list)
    
def move_from_unknown_to_known():
    """Takes the selected value in the known and unknown listbox and moves it between lists
    """
    known_list, unknown_list = get_known_and_unknown_lists()

    unknown_list, known_list = move_from_a_to_b(unknown_list, known_list, unknown_posts_list_box.curselection())

    set_known_and_unknown_lists(unknown_list, known_list)
    

def move_from_a_to_b(a: list, b: list, a_selections: tuple):
    """Moves elements from list a to list b

    Args:
        a (list): sending list
        b (list): reciving list
        a_selections (tuple): element to move from a to b

    Returns:
        list,list: the new a and b list 
    """
    if a_selections is ():
        return [],[]

    selected_ids = []
    for selected_index in a_selections:
        selected_ids.append(a[selected_index])

    for id in selected_ids:
        b.append(id)
        a.remove(id)

    a.sort()
    a.reverse()

    b.sort()
    b.reverse()
    
    return a, b
    
def get_known_and_unknown_lists():
    """Simply returns the known and unknown posts thats currently on the UI (NOT DATABASE)

    Returns:
        list, list: known, unknown posts list according to the UI
    """
    known_list = []
    unknown_list = []

    known_list = format_strvar_to_strlist(known_posts_list_var)
    unknown_list = format_strvar_to_strlist(unknown_posts_list_var)

    return known_list, unknown_list

def set_known_and_unknown_lists(unknown, known):
    """Sets the known and unknown listVar for the UI based on the inputted lists

    Args:
        unknown (list): list of str
        known (list): list of str
    """
    if unknown == [] and known == []:
        return
    
    known_posts_list_var.set(known)
    unknown_posts_list_var.set(unknown)

    # updating the database and user_obj
    user_id = id_entry_ele.get()
    service =  selected_service.get()

    user_obj = database.get_user_obj(user_id, service)

    # error checking to ensure the total values are still the same
    new_list = known + unknown
    new_list.sort()

    if user_obj.checked_post_ids == "": 
        user_obj.checked_post_ids = []
    if user_obj.unchecked_post_ids == "": 
        user_obj.unchecked_post_ids = []

    old_list = user_obj.checked_post_ids + user_obj.unchecked_post_ids #this returns int so need to convert to str
    old_list.sort()
    old_list = [ str(x) for x in old_list ]
    
    if new_list != old_list:
        logging.error("When trying to update the post lists, frontend != backend!")
        return

    user_obj.checked_post_ids = known
    user_obj.unchecked_post_ids = unknown

    database.update_database_row_user_object(user_obj)
    