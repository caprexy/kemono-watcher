"Tests for the two primary functions of the output controller"
import unittest
import sys
from unittest.mock import patch, Mock, MagicMock
import string

sys.path.append('../')
# pylint: disable=C0413
from testing import testConstants
from models.userModel import User
import checkerPanel.output_controller as output_controller
from checkerPanel.output_controller import get_unseen_post_ids_from_page

class OutputControllerTest(unittest.TestCase):
    """Test for the output controller. Should mock any external modules
    """

    @patch('urllib.request.urlopen')
    def test1_get_unseen_post_ids_from_page(self, urllib_mock):
        """Test the specific get_unseen_post_ids by giving a fake set of inputs 
            and also mocking the api call returns.
            We recreate situation where we check the first page and the user only has some checked ids
        """

        request = "https://kemono.party/api/" + testConstants.USER1_SERVICE + \
                    "/user/" + str(testConstants.USER1_ID) + "?o="

        with open(testConstants.USER1_FIRST_PAGE, 'rb') as file:
            entire_first_page_bytes = file.read()
        
        url_to_response_data = {
            request+"0": entire_first_page_bytes,
            request+"50": b"[]"
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
        known = testConstants.USER1_SECOND_HALF_POST_IDS[3:5]
        unknown = testConstants.USER1_SECOND_HALF_POST_IDS[5:]
        unseen = testConstants.USER1_SECOND_HALF_POST_IDS[:3]
    
        new_unseen = get_unseen_post_ids_from_page(request+str(api_index),
                        known, unknown, unseen)
        all_posts = known + unknown + unseen + new_unseen
        all_posts.sort()
        all_posts.reverse()

        assert all_posts == testConstants.USER1_FIRST_PAGE_IDS
        assert len(known) + len(unknown) + len(unseen) + len(new_unseen) == 50

    @patch("models.databaseModel.Database")
    @patch("inputPanel.statusHelper.setGetUpdatesStatusLabelValues")
    @patch("tkinter.Button")
    @patch('checkerPanel.output_controller.get_unseen_post_ids_from_page')
    def test2_get_unseen_posts_thread(self, 
            mock_get_unseen_post_ids, 
            mock_button, 
            mock_status_helper, 
            mock_database):
        """ Mocks the unseen posts, need to mock tons of external variable calls
        """
        # setup some extranous mocks that we may need
        output_controller.pass_vars(Mock(), mock_button, mock_database)
        update_user_data_mock = Mock()
        mock_database.updateUserData = update_user_data_mock
    
        # setup user1 data, seen/unseen/unknown variables
        user1_first_page = testConstants.USER1_FIRST_PAGE_IDS
        user1_first_page_unseen = [user1_first_page.pop(3)]
        user1_second_page = testConstants.USER1_SECOND_PAGE_IDS
        user1_second_page_unseen = [user1_second_page.pop(3)]
        
        user1_known = user1_first_page[5:] + user1_second_page[5:]
        user1_unknown = user1_first_page[:5] + user1_second_page[:5]
        user_obj_1 = User(
            1,
            testConstants.USER1_NAME,
            testConstants.USER1_ID,
            testConstants.USER1_SERVICE,
            user1_known,
            user1_unknown,
        )

        user2_first_page = testConstants.USER2_FIRST_PAGE_IDS
        user2_first_page_unseen = [user2_first_page.pop(3)]

        user2_known = user2_first_page[:5]
        user2_unknown = user2_first_page[5:]
        user_obj_2 = User(
            1,
            testConstants.USER2_NAME,
            testConstants.USER2_ID,
            testConstants.USER2_SERVICE,
            user2_known,
            user2_unknown,
        )
        mock_database.getAllUsersObj.return_value = [user_obj_1, user_obj_2]
        
        # we mock the result of this function call and just return as if this function works
        def mock_get_unseen_post_ids_side_effect(request: string,
                            known_ids: list,
                            unknown_ids: list,
                            unseen_ids: list):
            if request == "https://kemono.party/api/" + testConstants.USER1_SERVICE + \
                    "/user/" + str(testConstants.USER1_ID) + "?o=0":
                return user1_first_page_unseen
            elif request == "https://kemono.party/api/" + testConstants.USER1_SERVICE + \
                    "/user/" + str(testConstants.USER1_ID) + "?o=50":
                return user1_second_page_unseen
            elif request == "https://kemono.party/api/" + testConstants.USER2_SERVICE + \
                    "/user/" + str(testConstants.USER2_ID) + "?o=0":
                return user2_first_page_unseen
            else:
                return []
        mock_get_unseen_post_ids.side_effect = mock_get_unseen_post_ids_side_effect
        
        output_controller.get_unread_posts_thread()
        
        user_1_sorted_unknown = user1_unknown + user1_first_page_unseen + user1_second_page_unseen
        user_1_sorted_unknown.sort()
        user_2_sorted_unknown = user2_unknown + user2_first_page_unseen
        user_2_sorted_unknown.sort()

        expected_calls = [
                (testConstants.USER1_ID,
                    testConstants.USER1_SERVICE,
                    user1_known,
                    user_1_sorted_unknown),
                (testConstants.USER2_ID,
                    testConstants.USER2_SERVICE,
                    user2_known,
                    user_2_sorted_unknown)
            ]

        actual_calls = list(call_args[0] for call_args in update_user_data_mock.call_args_list)
        assert expected_calls == actual_calls
