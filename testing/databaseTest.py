import unittest
import sys
import os
from unittest.mock import patch, Mock, MagicMock
import testConstants
import threading
import json

sys.path.append('../')

import models.databaseModel as database
from inputPanel import statusHelper
import constants

class databaseTests(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.database = database.Database()

        # sample user data
        cls.databaseId = 72813
        cls.name = "na"
        cls.service = "Patreon"
        cls.checked_post_ids = [84905474, 84778099, 84238287, 83529449, 83343026, 83218897, 83169653, 83065295, 82276738, 82064413, 81954654, 81851518, 81209841, 81059547, 80704628, 80338946, 80190808, 79994633, 78434719, 77440488, 76755887, 75926672, 75710038, 75580104, 75157411, 75022239, 74916213, 74693973, 74245334, 74158934, 73468219, 73194386, 72942785, 72646675, 72467685, 72405353, 72310762, 72205399, 72091429, 72030404, 72001916, 71756991, 71677434, 71623437, 71380943, 71238640, 71182880, 71135747, 71087979, 71070581, 71062351, 70996043, 70943219, 70897713, 70853491, 70808920, 70769224, 70745940, 70716118, 70668831, 70668428, 70661972, 70605413, 70568003, 70527415, 70526592, 70489194, 70114372, 69844726, 69806320, 69437650, 69267254, 68972303, 68433820, 68341058, 68202290, 68113175, 68024574, 67908936, 67606882, 67436555, 67305910, 67104339, 66932176, 66803019, 66689004, 66646000, 66438173, 66382705, 66218736, 66063628, 65980003, 65911698, 65731008, 65424136, 65392885, 65214407, 64974747, 64968926, 64828106]
        cls.unchecked_post_ids = []

        cls.idTwo = 645
        cls.idOne = 233
    
    @classmethod
    def tearDownClass(cls):
        cls.database.close_all_connections()
        if os.path.exists(constants.DATABASE_FILENAME):
            os.remove(constants.DATABASE_FILENAME)

    # everything needs to be tested as multithreaded because need a thread to display interface and run stuff
    def test1CreateTwoUsers(self):
        print("Creating users")
        with patch('inputPanel.statusHelper.setuserOperationStatusValues') as mock_statusHelper, \
             patch('urllib.request.urlopen', side_effect=self.side_effect_apiCall) as mock_urlopen:
            
            print("Multithreading creation calls")
            t1 = threading.Thread(target=self.createTestUser, args=(self.idOne,))

            t2 = threading.Thread(target=self.createTestUser, args=(self.idTwo,))
            t1.start()
            t2.start()
            
            t2.join()
            t1.join()
            print("Joined, both users created")
            print("Getting all users")

    def side_effect_apiCall(self, url, *args, **kwargs):  # Accept extra arguments
        mock_res = MagicMock()
        if url.endswith("=0"):
            with open(testConstants.USER1_FIRST_PAGE, 'rb') as file:
                sample_api_bytes = file.read()
            mock_res.read.return_value = sample_api_bytes
        elif url.endswith("50"):
            with open(testConstants.USER1_SECOND_PAGE, 'rb') as file:
                sample_api_bytes = file.read()
            mock_res.read.return_value = sample_api_bytes
        else:
            mock_res.read.return_value = b'{}'
        return mock_res

    def createTestUser(self, id):
        buttonMock = MagicMock()

        self.database.create_user(
            id,
            self.service,
            buttonMock
        )

    def test2GetAllUsersMethods(self):
        print("Testing if users were sucessfully added/ can get all users (and their objs)")
        res = self.database.get_all_user_id_and_services()
        
        #checking values
        self.assertEqual(len(res),2)

        if res[0][0] not in [self.idOne, self.idTwo]:
            raise ValueError("the id is incorrect")
        
        res = self.database.get_all_user_obj()
        self.assertEqual(len(res),2)
        rowTupleResOne = res[0].get_as_row_tuple()
        rowTupleTruth = (rowTupleResOne[0], #id value depends on which one was added first by multithreading, wholy unimportant
                      self.name, 
                      rowTupleResOne[2], 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))
        assert rowTupleResOne == rowTupleTruth

    def test3get_user_obj(self):
        print("Testing if can get specific user and data")
        res = self.database.get_user_obj(self.idOne, self.service)
        rowTupleResOne = res.get_as_row_tuple()
        rowTupleTruth = (rowTupleResOne[0],  
                      self.name, 
                      self.idOne, 
                      self.service, 
                      json.dumps(self.checked_post_ids), 
                      json.dumps(self.unchecked_post_ids))
        assert rowTupleResOne == rowTupleTruth

    def test4UpdateUserObj(self):
        print("Replacing/updating row based on database id")
        userObj = self.database.get_user_obj(self.idOne, self.service)

        userObj.checked_post_ids = []
        userObj.id = 1337
        self.database.update_database_row_user_object(userObj)

        userObj = self.database.get_user_obj(1337, self.service)
        assert userObj.id == 1337
        assert userObj.checked_post_ids == []
        assert self.database.does_user_exist(self.idOne, self.service) == False
        self.idOne = userObj.id

        print("Updating without making a new user object")
        self.database.update_database_row_manual_input(self.idOne, self.service, [1], [2])
        userObj = self.database.get_user_obj(self.idOne, self.service)
        
        assert userObj.checked_post_ids == [1]
        assert userObj.unchecked_post_ids == [2]

    def test5KnowAllUnknownPosts(self):
        print("Testing convert all unknown to known posts")
        self.database.update_database_row_manual_input(self.idTwo, self.service, [1], [2,3,4])
        self.database.know_unknown_post(self.idTwo, self.service, 2)
        self.database.know_unknown_post(self.idTwo, self.service, 4)
        
        with self.assertRaises(KeyError):
            self.database.know_unknown_post(self.idTwo, self.service, 5)
        assert self.database.get_user_obj(self.idTwo, self.service).unchecked_post_ids == [3]

    @patch('inputPanel.statusHelper.setuserOperationStatusValues')
    def test6delete_user(self, patch_statusHelper):
        print("Testing delete user")
        self.database.delete_user(self.idTwo, self.service)
        assert self.database.get_user_obj(self.idOne, self.service) == None
    

if __name__ == '__main__':

    unittest.main()