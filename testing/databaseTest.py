import unittest
import sys
import os
import tkinter as tk
from unittest.mock import patch, Mock, MagicMock
import urllib.request
import testConstants
import http.client
import threading
import json
import functools

sys.path.append('../')

import models.databaseModel as database
from inputPanel import statusHelper
import constants

class databaseTests(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.database = database.Database()

        # sample user data
        cls.databaseId = 2
        cls.name = "na"
        cls.service = "Patreon"
        cls.checkedPostIds = [84905474,84778099,84238287,83529449,83343026,83218897,83169653,83065295,82276738,82064413,81954654,81851518,81209841,81059547,80704628,80338946,80190808,79994633,78434719,77440488,76755887,75926672,75710038,75580104,75157411,75022239,74916213,74693973,74245334,74158934,73468219,73194386,72942785,72646675,72467685,72405353,72310762,72205399,72091429,72030404,72001916,71756991,71677434,71623437,71380943,71238640,71182880,71135747,71087979,71070581]
        cls.uncheckedPostIds = []

        cls.idTwo = 645
        cls.idOne = 233
    
    @classmethod
    def tearDownClass(cls):
        cls.database.closeAllConnections()
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
            with open(testConstants.apiSampleCallBytesLocation, 'rb') as file:
                sample_api_bytes = file.read()
            mock_res.read.return_value = sample_api_bytes
        elif url.endswith("50"):
            mock_res.read.return_value = b'{}'
        else:
            raise ValueError("Unexpected url: " + url)
        return mock_res

    def createTestUser(self, id):
        buttonMock = MagicMock()

        self.database.createUser(
            id,
            self.service,
            buttonMock
        )

    def test2GetAllUsersMethods(self):
        print("Testing if users were sucessfully added/ can get all users (and their objs)")
        res = self.database.getAllUserIdServices()
        
        #checking values
        self.assertEqual(len(res),2)

        if res[0][0] not in [self.idOne, self.idTwo]:
            raise ValueError("the id is incorrect")
        
        res = self.database.getAllUsersObj()
        self.assertEqual(len(res),2)

        rowTupleResOne = res[0].getAsRowTuple()
        rowTupleTruth = (rowTupleResOne[0], #id value depends on which one was added first by multithreading, wholy unimportant
                      self.name, 
                      rowTupleResOne[2], 
                      self.service, 
                      json.dumps(self.checkedPostIds), 
                      json.dumps(self.uncheckedPostIds))
        assert rowTupleResOne == rowTupleTruth

    def test3GetUserObj(self):
        print("Testing if can get specific user and data")
        res = self.database.getUserObj(self.idOne, self.service)
        rowTupleResOne = res.getAsRowTuple()
        rowTupleTruth = (rowTupleResOne[0],  
                      self.name, 
                      self.idOne, 
                      self.service, 
                      json.dumps(self.checkedPostIds), 
                      json.dumps(self.uncheckedPostIds))
        assert rowTupleResOne == rowTupleTruth

    def test4UpdateUserObj(self):
        print("Replacing/updating row based on database id")
        userObj = self.database.getUserObj(self.idOne, self.service)

        userObj.checkedPostIds = []
        userObj.id = 1337
        self.database.replaceDatabaseIdRow(userObj)

        userObj = self.database.getUserObj(1337, self.service)
        assert userObj.id == 1337
        assert userObj.checkedPostIds == []
        assert self.database.userExists(self.idOne, self.service) == False
        self.idOne = userObj.id

        print("Updating without making a new user object")
        self.database.updateUserData(self.idOne, self.service, [1], [2])
        userObj = self.database.getUserObj(self.idOne, self.service)
        
        assert userObj.checkedPostIds == [1]
        assert userObj.uncheckedPostIds == [2]

    def test5KnowAllUnknownPosts(self):
        print("Testing convert all unknown to known posts")
        self.database.updateUserData(self.idTwo, self.service, [1], [2,3,4])
        self.database.knowUnknownPost(self.idTwo, self.service, 2)
        self.database.knowUnknownPost(self.idTwo, self.service, 4)
        
        with self.assertRaises(KeyError):
            self.database.knowUnknownPost(self.idTwo, self.service, 5)
        assert self.database.getUserObj(self.idTwo, self.service).uncheckedPostIds == [3]

    @patch('inputPanel.statusHelper.setuserOperationStatusValues')
    def test6DeleteUser(self, patch_statusHelper):
        print("Testing delete user")
        self.database.deleteUser(self.idTwo, self.service)
        assert self.database.getUserObj(self.idOne, self.service) == None
    

if __name__ == '__main__':

    unittest.main()