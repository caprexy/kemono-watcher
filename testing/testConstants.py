"Constants for testing"
import json

def generate_post_ids_from_bin(binFile : str)-> list[str]:
    """This reads a bin file/basically json, and turns it into a sequence of ids

    Args:
        binFile (str): The output of Kemono's api

    Returns:
        list[int]: the ids to be used
    """
    id_list = []
    with open(binFile, 'rb') as contents:
        res = json.loads(contents.read().decode())
        for obj in res:
            id_list.append(int(obj["id"]))
    return id_list

# sample real user
# https://kemono.party/patreon/user/72813
USER1_NAME = "Shencomix"
USER1_SERVICE = "Pateron"
USER1_ID = 72813
USER1_FIRST_PAGE = "shen_post_api_page_one.bin"
USER1_SECOND_PAGE = "shen_post_api_page_two.bin"
USER1_FIRST_PAGE_IDS = generate_post_ids_from_bin(USER1_FIRST_PAGE)
USER1_SECOND_PAGE_IDS = generate_post_ids_from_bin(USER1_SECOND_PAGE)
USER1_FIRST_HALF_FIRST_PAGE = "shen_post_api_page_one_first_half.json"
USER1_SECOND_HALF_FIRST_PAGE = "shen_post_api_page_one_second_half.json"
USER1_FIRST_HALF_POST_IDS = generate_post_ids_from_bin(USER1_FIRST_HALF_FIRST_PAGE)
USER1_SECOND_HALF_POST_IDS = generate_post_ids_from_bin(USER1_SECOND_HALF_FIRST_PAGE)

# user 2
# https://kemono.party/patreon/user/9210140
USER2_NAME = "Liliuhms"
USER2_SERVICE = "Pateron"
USER2_ID = 9210140
USER2_FIRST_PAGE = "liliuhms_post_api_page_one.bin"
USER2_FIRST_PAGE_IDS = generate_post_ids_from_bin(USER2_FIRST_PAGE)
