"""Test file for database in models"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import threading
import json


# pylint: disable=C0411

sys.path.append('../')
from testing import local_constants

import models.database_model as database
import constants
      
class DatabaseTests(unittest.TestCase):
    """Is a standard unittest module for the database in the database_model module"""
        
    @classmethod
    def setUpClass(cls):
        cls.database = database.Database()

        # sample user data
        cls.databaseId = 72813
        cls.name = "na"
        cls.service = "Patreon"
        cls.checked_post_ids = [84905474, 84778099, 84238287, 83529449, 83343026, 83218897, 83169653, 83065295, 82276738, 82064413, 81954654, 81851518, 81209841, 81059547, 80704628, 80338946, 80190808, 79994633, 78434719, 77440488, 76755887, 75926672, 75710038, 75580104, 75157411, 75022239, 74916213, 74693973, 74245334, 74158934, 73468219, 73194386, 72942785, 72646675, 72467685, 72405353, 72310762, 72205399, 72091429, 72030404, 72001916, 71756991, 71677434, 71623437, 71380943, 71238640, 71182880, 71135747, 71087979, 71070581, 71062351, 70996043, 70943219, 70897713, 70853491, 70808920, 70769224, 70745940, 70716118, 70668831, 70668428, 70661972, 70605413, 70568003, 70527415, 70526592, 70489194, 70114372, 69844726, 69806320, 69437650, 69267254, 68972303, 68433820, 68341058, 68202290, 68113175, 68024574, 67908936, 67606882, 67436555, 67305910, 67104339, 66932176, 66803019, 66689004, 66646000, 66438173, 66382705, 66218736, 66063628, 65980003, 65911698, 65731008, 65424136, 65392885, 65214407, 64974747, 64968926, 64828106]
        cls.unchecked_post_ids = []

        cls.id_two = 645
        cls.id_one = 233
    
    @classmethod
    def tearDownClass(cls):
        cls.database.close_all_connections()
        if os.path.exists(constants.DATABASE_FILENAME):
            os.remove(constants.DATABASE_FILENAME)

        
    def test1_create_two_users(self):
        """Run a test to create two uses in parallel. 
            Wanted to be parallel since the primary UI thread cannot be frozen.
        """ 
        print("Creating 2 users")

        
        
        button_mock = MagicMock()
        def create_test_user(user_id:int):
            """Function to be called for the threading

            Args:
                id (int): id to be passed in
            """

            self.database.create_user(
                user_id,
                self.service,
                button_mock
            )

        with patch('input_panel.status_helper.set_user_operation_status_values'), \
             patch('urllib.request.urlopen') as mock_urlopen:
            
            # passing along the url to the PretendContext
            mock_urlopen.side_effect = lambda url: PretendContext(url)

            print("Multithreading creation calls")
            thread_1 = threading.Thread(target=create_test_user, args=(self.id_one,))

            thread_2 = threading.Thread(target=create_test_user, args=(self.id_two,))
            thread_1.start()
            thread_2.start()
            
            thread_2.join()
            thread_1.join()
            print("Joined, both users created")
            
            print("Testing malformed inputs")
            with self.assertRaises(ValueError):
                self.database.create_user("id","Pateron", button_mock)
            with self.assertRaises(AssertionError):
                self.database.create_user(5,"service", button_mock)


    def test2_get_all_users_methods(self):
        """Tests the get_all_users method and get_all_user_id_and_services 

        Raises:
            ValueError: In the case of unexpected/incorrect ids
        """
        print("Testing if users were sucessfully added/ can get all users (and their objs)")
        res = self.database.get_all_user_id_and_services()
        
        #checking values
        self.assertEqual(len(res),2)
        assert isinstance(res[0][0], int)
        assert isinstance(res[0][1], str)
        if res[0][0] not in [self.id_one, self.id_two]:
            raise ValueError("the id is incorrect")
        
        res = self.database.get_all_user_obj()
        self.assertEqual(len(res),2)
        row_tuple_res_0 = res[0].get_as_row_tuple()
        row_tuple_truth = (row_tuple_res_0[0], 
            #id value depends on which one was added first by multithreading, so needs to be set
                      self.name, 
                      row_tuple_res_0[2], 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))
        assert row_tuple_res_0 == row_tuple_truth

    def test3_get_user_obj(self):
        """Tests the get_user_obj function and thus does_user_exist since it calls get_user_obj
        Also testing based on database id
        """
        print("Testing if can get specific user and data")
        res = self.database.get_user_obj(self.id_one, self.service)
        row_tuple_res_0 = res.get_as_row_tuple()
        row_tuple_truth = (row_tuple_res_0[0],  
                      self.name, 
                      self.id_one, 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))
        assert row_tuple_res_0 == row_tuple_truth

        res = self.database.get_user_from_database_id(self.databaseId)
        assert row_tuple_res_0 == row_tuple_truth

    def test4_update_user_obj(self):
        """Tests the update_user_obj using the manual input and object input
        """
        print("Replacing/updating row based on database id and user object")
        user_obj = self.database.get_user_obj(self.id_one, self.service)

        user_obj.checked_post_ids = []
        self.database.update_database_row_user_object(user_obj)

        user_obj = self.database.get_user_obj(self.id_one, self.service)
        assert user_obj.checked_post_ids == []
        self.id_one = user_obj.id

        print("Updating without making a new user object")
        self.database.update_database_row_manual_input(self.id_one, self.service, [1], [2])
        user_obj = self.database.get_user_obj(self.id_one, self.service)
        
        assert user_obj.checked_post_ids == [1]
        assert user_obj.unchecked_post_ids == [2]

        print("Testing attempting to update a nonexisting object or other edge cases")
        # nonexistant keys like database id, id, service
        user_obj = self.database.get_user_obj(self.id_one, self.service)
        user_obj.database_id = -1
        with self.assertRaises(AssertionError):
            self.database.update_database_row_user_object(user_obj)

        with self.assertRaises(AssertionError):
            self.database.update_database_row_manual_input(-1, self.service, [1], [2])
        with self.assertRaises(AssertionError):
            self.database.update_database_row_manual_input(self.id_one, "service", [1], [2])
        
    def test5_get_all_unknown_posts(self):
        """Testing specific get all unkown posts function and services
        """
        print("Testing getting all unknown posts")
        self.database.update_database_row_manual_input(self.id_two, self.service, [1], [2,3,4])
        self.database.update_database_row_manual_input(self.id_one, self.service, [3], [1,3,5])

        res = self.database.get_all_uknown_post_ids_and_service()
        for post in res:
            post = post.split(",")
            post[0] = int(post[0])
            post[2] = int(post[2])
            
            assert post[0] in [1,2,3,4,5], "Misread the unknown posts somehow?"
            assert post[1] == self.service, "Wrong service"
            assert post[2] in [self.id_one, self.id_two]


    
    def test6_know_all_unknown_posts(self):
        """Making sure we can convert a known post into unknown, maybe should make other half 
        """
        print("Testing convert all unknown to known posts")
        self.database.update_database_row_manual_input(self.id_two, self.service, [1], [2,3,4])
        self.database.know_unknown_post(self.id_two, self.service, 2)
        self.database.know_unknown_post(self.id_two, self.service, 4)
        
        with self.assertRaises(KeyError):
            self.database.know_unknown_post(self.id_two, self.service, 5)
        assert self.database.get_user_obj(self.id_two, self.service).unchecked_post_ids == [3]

    @patch('input_panel.status_helper.set_user_operation_status_values')
    def test7_delete_user(self, patch_status_helper):
        """Tests deleting a user function
        """
        print("Testing delete user")
        self.database.delete_user(self.id_one, self.service)
        assert self.database.get_user_obj(self.id_one, self.service) is None
    

class PretendContext:
    """This is a fake context manager for urlopen, thus we can control what the result of 
       read is 
    """
    def __init__(self, url):
        self.url = url
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self) -> bytes:
        """A function to mock the api call. It takes in a url and returns different
        bytes based on the input url. 

        Returns:
            bytes: output bytes based on what it theoretically should've
        """
        if self.url.endswith("=0"):
            with open(local_constants.USER1_FIRST_PAGE, 'rb') as file:
                sample_api_bytes = file.read()
                return sample_api_bytes
        elif self.url.endswith("50"):
            with open(local_constants.USER1_SECOND_PAGE, 'rb') as file:
                sample_api_bytes = file.read()
                return sample_api_bytes
        else:
            return b'{}'
  
if __name__ == '__main__':

    unittest.main()
