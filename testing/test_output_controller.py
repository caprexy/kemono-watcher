"Tests for the two primary functions of the output controller"
import unittest
import sys
from unittest.mock import patch, Mock, MagicMock
import string

sys.path.append('../')
# pylint: disable=C0413
from models.user_model import User
from output_panel import output_controller
from output_panel.output_controller import get_unseen_post_ids_from_page
from testing import local_constants
# pylint: enable=C0413

class OutputControllerTest(unittest.TestCase):
    """Test for the output controller. Should mock any external modules
    """

    @patch('urllib.request.urlopen')
    def test1_get_unseen_post_ids_from_page(self, urllib_mock):
        """Test the specific get_unseen_post_ids by giving a fake set of inputs 
            and also mocking the api call returns.
            We recreate situation where we check the first page and the user only has some checked ids
        """
        print("Testing if we can process an api call and get new ones")
        request = "https://kemono.party/api/" + local_constants.USER1_SERVICE + \
                    "/user/" + str(local_constants.USER1_ID) + "?o="

        with open(local_constants.USER1_FIRST_PAGE, 'rb') as file:
            entire_first_page_bytes = file.read()
        
        url_to_response_data = {
            request+"0": entire_first_page_bytes,
            request+"50": b"[]\n"
        }

        # returning a mock to handle the read call
        # enter/exit required due to the with as statement
        def urlopen_side_effect(url, *args, **kwargs): 
            mock_response = MagicMock()

            mock_response.__enter__.return_value = mock_response
            mock_response.__exit__.return_value = False
            mock_response.read.return_value = url_to_response_data.get(url)

            return mock_response
        urllib_mock.side_effect = urlopen_side_effect

        api_index = 0
        # Using second half of the first page bc logically unseen content is probably new
        known = local_constants.USER1_SECOND_HALF_POST_IDS[3:5]
        unknown = local_constants.USER1_SECOND_HALF_POST_IDS[5:]
        unseen = local_constants.USER1_SECOND_HALF_POST_IDS[:3]
    
        new_unseen = get_unseen_post_ids_from_page(request+str(api_index),
                        known, unknown, unseen)
        
        # type checking
        assert isinstance(new_unseen, list)
        assert isinstance(new_unseen[0], int)
        
        all_posts = known + unknown + unseen + new_unseen
        all_posts.sort()
        all_posts.reverse()

        assert all_posts == local_constants.USER1_FIRST_PAGE_IDS
        assert len(known) + len(unknown) + len(unseen) + len(new_unseen) == 50

        # testing the empty case
        api_index += 50
        new_unseen = get_unseen_post_ids_from_page(request+str(api_index),
                known, unknown, unseen)
        assert not new_unseen

    @patch("models.database_model.Database")
    @patch("input_panel.status_helper.set_get_updates_status_label_values")
    @patch("tkinter.Button")
    @patch('output_panel.output_controller.get_unseen_post_ids_from_page')

    def test2_get_unseen_posts_thread(self, 
            mock_get_unseen_post_ids, 
            mock_button, 
            mock_status_helper, 
            mock_database):
        """ Mocks the unseen posts, need to mock tons of external variable calls
        """
        print("Testing getting unseen post ids through database and api calls")
        # setup some extranous mocks that we may need
        output_controller.pass_vars(Mock(), mock_button, mock_database)
        update_user_data_mock = Mock()
        mock_database.update_database_row_manual_input = update_user_data_mock
    
        # setup user1 data, seen/unseen/unknown variables
        user1_first_page = local_constants.USER1_FIRST_PAGE_IDS
        user1_first_page_unseen = [user1_first_page.pop(3)]
        user1_second_page = local_constants.USER1_SECOND_PAGE_IDS
        user1_second_page_unseen = [user1_second_page.pop(3)]
        
        user1_known = user1_first_page[5:] + user1_second_page[5:]
        user1_unknown = user1_first_page[:5] + user1_second_page[:5]
        user_obj_1 = User(
            1,
            local_constants.USER1_NAME,
            local_constants.USER1_ID,
            local_constants.USER1_SERVICE,
            user1_known,
            user1_unknown,
        )

        user2_first_page = local_constants.USER2_FIRST_PAGE_IDS
        user2_first_page_unseen = [user2_first_page.pop(3)]

        user2_known = user2_first_page[:5]
        user2_unknown = user2_first_page[5:]
        user_obj_2 = User(
            1,
            local_constants.USER2_NAME,
            local_constants.USER2_ID,
            local_constants.USER2_SERVICE,
            user2_known,
            user2_unknown,
        )
        mock_database.get_all_user_obj.return_value = [user_obj_1, user_obj_2]
        
        # we mock the result of this function call and just return as if this function works
        def mock_get_unseen_post_ids_side_effect(request: string,
                            known_ids: list,
                            unknown_ids: list,
                            unseen_ids: list):
            if request == "https://kemono.party/api/" + local_constants.USER1_SERVICE + \
                    "/user/" + str(local_constants.USER1_ID) + "?o=0":
                return user1_first_page_unseen
            if request == "https://kemono.party/api/" + local_constants.USER1_SERVICE + \
                    "/user/" + str(local_constants.USER1_ID) + "?o=50":
                return user1_second_page_unseen
            if request == "https://kemono.party/api/" + local_constants.USER2_SERVICE + \
                    "/user/" + str(local_constants.USER2_ID) + "?o=0":
                return user2_first_page_unseen
            return []
        mock_get_unseen_post_ids.side_effect = mock_get_unseen_post_ids_side_effect
        
        output_controller.get_unread_posts_thread()
        
        user_1_sorted_unknown = user1_unknown + user1_first_page_unseen + user1_second_page_unseen
        user_1_sorted_unknown.sort()
        user_2_sorted_unknown = user2_unknown + user2_first_page_unseen
        user_2_sorted_unknown.sort()

        expected_calls = [
                (local_constants.USER1_ID,
                    local_constants.USER1_SERVICE,
                    user1_known,
                    user_1_sorted_unknown),
                (local_constants.USER2_ID,
                    local_constants.USER2_SERVICE,
                    user2_known,
                    user_2_sorted_unknown)
            ]

        actual_calls = list(call_args[0] for call_args in update_user_data_mock.call_args_list)
        assert expected_calls == actual_calls
