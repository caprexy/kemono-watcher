""" Tests for the user model"""
import unittest
import sys
import json

sys.path.append('../')

import models.userModel as userModel

#python -m unittest userTest.py
class UserTests(unittest.TestCase):
    """Test class for user

    Args:
        unittest (_type_): standard input
    """
        
    def setUp(self):
        """ Provides hardcoded data for a user
        """
        self.database_id = 2
        self.name = "yellow"
        self.id = "2234"
        self.service = "Patreon"
        self.checked_post_ids = [1,5,4,6,75]
        self.unchecked_post_ids = [2,3,7,99]

        self.user = userModel.User(self.database_id, self.name, self.id, self.service, self.checked_post_ids, self.unchecked_post_ids)

        self.assertEqual(self.user.database_id, self.database_id)
        self.assertEqual(self.user.name, self.name)


    def test1_get_as_row_tuple(self):
        """simple hardcodes a expected uple for the user data set in setUp
        """
        tuple_results = self.user.get_as_row_tuple()
        tuple_truth = (self.database_id, 
                      self.name, 
                      self.id, 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))

        self.assertEqual(tuple_results, tuple_truth)

    def test2_convert_row_to_user(self):
        """Depends on test1 being accurate since it uses get_as_row_tuple function
        """
        tuple_results = self.user.get_as_row_tuple()
        user_result = userModel.convert_row_to_user(tuple_results)
        
        assert isinstance(self.user, userModel.User)
        self.assertEqual(self.user.database_id, user_result.database_id)
        self.assertEqual(self.user.name, user_result.name)