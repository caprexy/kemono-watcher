""" Contains all methods to modify the status labels"""
DEFAULT_BG_COLOR = "#f0f0f0"

# pylint: disable=C0103
user_operation_status_label = None
# pylint: enable=C0103

def set_user_operation_status_label(user_operation_status_label_in):
    """Sets the status label to be modified by status_helper

    Args:
        user_operation_status_label_in (_type_): status label to be used
    """
    global user_operation_status_label
    user_operation_status_label = user_operation_status_label_in

def set_user_operation_status_values(label_text, bg_color="default"):
    """Sets the values for the operation status label

    Args:
        label_text (_type_): text to be displayed
        bg_color (str, optional): color to be displayed. Defaults to "default".
    """
    if bg_color == "default":
        user_operation_status_label.config(text=label_text, bg = DEFAULT_BG_COLOR)
        return
    user_operation_status_label.config(text=label_text, bg = bg_color)

def clear_user_operation_status():
    """Clears the user operation status label
    """
    user_operation_status_label.config(text="", bg = DEFAULT_BG_COLOR)

# pylint: disable=C0103
get_updates_status_label = None
# pylint: enable=C0103

def set_get_updates_status_label(get_updates_status_label_in):
    """Sets the update status label to be modified

    Args:
        get_updates_status_label_in (_type_): update status label to be used
    """
    global get_updates_status_label
    get_updates_status_label = get_updates_status_label_in


def set_get_updates_status_label_values(label_text, bg_color="default"):
    """Sets the values for the update status label

    Args:
        label_text (_type_): text to be displayed
        bg_color (str, optional): color to be displayed. Defaults to "default".
    """
    if bg_color == "default":
        get_updates_status_label.config(text=label_text, bg = DEFAULT_BG_COLOR)
        return
    get_updates_status_label.config(text=label_text, bg = bg_color)

def clear_get_updates_status_label():
    """Clears the get update status label
    """
    get_updates_status_label.config(text="", bg = DEFAULT_BG_COLOR)
