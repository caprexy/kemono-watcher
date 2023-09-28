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
        cls.name = "yellow"
        cls.service = "Patreon"
        cls.checkedPostIds = [1,5,4,6,75]
        cls.uncheckedPostIds = [2,3,7,99]

        cls.idTwo = 645
        cls.idOne = 233
    
    @classmethod
    def tearDownClass(cls):
        cls.database.closeAllConnections()
        if os.path.exists(constants.DATABASE_FILENAME):
            os.remove(constants.DATABASE_FILENAME)

    # everything needs to be tested as multithreaded because need a thread to display interface and run stuff
    def testCreateTwoUsers(self):
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

    def testGetUsers(self):
        print("Testing if users were sucessfully added/ can get all users")
        res = self.database.getAllUserIdServices()
        
        #checking values
        self.assertEqual(len(res),2)

        if(res[0][0] != self.idOne and res[0][0] != self.idTwo):
            raise ValueError("the id is incorrect")

def custom_test_order(test_case, test_name):
    # Define a custom sorting function to control the order
    order = {
        'testCreateTwoUsers': 1,
        'testGetUsers': 2,
    }
    return order.get(test_name, 0)

    

if __name__ == '__main__':
    # Set the custom sorting function for the test case
    unittest.TestLoader.sortTestMethodsUsing = custom_test_order

    unittest.main()