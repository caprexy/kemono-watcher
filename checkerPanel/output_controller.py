"Controller/busniess logic of the output view/right panel of the application"
import threading
import urllib.request
import json
from tkinter import StringVar, Button
import string

from models.databaseModel import Database
from inputPanel import status_helper

# pylint: disable=C0103
new_posts_list_var = None
update_posts_button = None
database = None
# pylint: enable=C0103


def pass_vars(new_posts_list_var_in : StringVar, 
              update_posts_button_in : Button, 
              database_in : Database):
    """Sets variables from the output view to be used by the controller

    Args:
        new_posts_list_var_in (StringVar): needed to get selected new posts
        update_posts_button_in (Button): needed so we can enable and disable button as desired
        database_in (Database): need database to operate on
    """
    global new_posts_list_var, update_posts_button, database
    new_posts_list_var = new_posts_list_var_in
    update_posts_button = update_posts_button_in
    database = database_in    

# define a function to get api post ids
def get_unseen_post_ids_from_page(request: string,
                        known_ids: list[int],
                        unknown_ids: list[int],
                        known_unseen_ids: list[int]) -> list[int]:
    """Get new posts that we do not yet know about

    Args:
        request (int): api request string
        known_ids(list[int]): in database and user has seen
        unknown_ids(list[int]): these ids already exist in the database but are simply marked as unseen by user
        known_unseen_ids (list[int]): known posts we didnt know about previously, avoid adding again

    Returns:
        list[str]: all new unseen posts to be added to database
    """
    with urllib.request.urlopen(request) as contents:
        data = contents.read()
        response = json.loads(data.decode())

        if response==[]: 
            return []

        api_post_ids = []
        for obj in response:
            api_post_ids.append(int(obj["id"]))

        new_unseen_posts = []
        for post_id in api_post_ids:
            if(post_id not in known_ids
                and post_id not in unknown_ids
                and post_id not in known_unseen_ids):
                new_unseen_posts.append(post_id)
    return new_unseen_posts
    
def get_unread_posts():
    """Puts the threading logic in the controller
    """
    threading.Thread(target=get_unread_posts_thread).start()
def get_unread_posts_thread():
    """ Will attempt to get all unread/unknown posts.
        First, checking the database of already known/unknown posts.
        Then will try to make api calls to find any new unread posts
    """

    update_posts_button.config(state="disabled")
    unknown_posts = database.get_all_uknown_post_ids_and_service()
    new_posts_list_var.set(unknown_posts)
    status_helper.set_get_updates_status_label_values("Got database unknown posts!", "orange")

    ## Fetch api, compare posts to find new posts, if neeeded update new_posts_list_var
    update_posts_button.config(state="normal")

    users = database.get_all_user_obj()
    for user in users:
        service = user.service
        user_id = user.id
        status_helper.set_get_updates_status_label_values(
            "Getting posts from "+service+" for id:"+str(user_id), "orange")
        
        api_index=0
        request = "https://kemono.party/api/" + service + \
                    "/user/" + str(user_id) + "?o="
        id_list = []
        unseen_ids = []
        known_ids = user.checked_post_ids
        unknown_ids = user.unchecked_post_ids

        id_list += get_unseen_post_ids_from_page(request+str(api_index), known_ids, unknown_ids, unseen_ids)
        unseen_ids += id_list
        # if we found some unseen posts, check all pages until we no longer find unseen posts
        if len(id_list) != 0:
            while len(id_list) != 0: #keep running while api responses exists
                api_index += 50
                id_list= get_unseen_post_ids_from_page(request+str(api_index), known_ids, unknown_ids, unseen_ids)
                unseen_ids += id_list
        new_unknown = unknown_ids+unseen_ids
        new_unknown.sort()
        
        database.update_database_row_manual_input(user_id, service, known_ids, new_unknown)
    
    unknown_posts = database.get_all_uknown_post_ids_and_service()
    new_posts_list_var.set(unknown_posts)
    status_helper.set_get_updates_status_label_values("Finished getting posts from web", "green")
