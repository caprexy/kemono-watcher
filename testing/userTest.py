import unittest
import sys
import json

sys.path.append('../')

import models.userModel as userModel

#python -m unittest userTest.py
class userTests(unittest.TestCase):
        
    def setUp(self):
        self.databaseId = 2
        self.name = "yellow"
        self.id = "2234"
        self.service = "Patreon"
        self.checkedPostIds = [1,5,4,6,75]
        self.uncheckedPostIds = [2,3,7,99]

        self.user = userModel.User(self.databaseId, self.name, self.id, self.service, self.checkedPostIds, self.uncheckedPostIds)
        self.assertIsInstance(self.user, userModel.User)
    
        self.assertEqual(self.user.databaseId, self.databaseId)
        self.assertEqual(self.user.name, self.name)


    def testGetAsRowTuple(self):
        tupleResults = self.user.getAsRowTuple()
        tupleTruth = (self.databaseId, 
                      self.name, 
                      self.id, 
                      self.service, 
                      json.dumps(self.checkedPostIds), 
                      json.dumps(self.uncheckedPostIds))

        self.assertEqual(tupleResults, tupleTruth)

    def testRowIntoUser(self):
        tupleResults = self.user.getAsRowTuple()
        userResults = userModel.convertRowIntoUser(tupleResults)

        self.assertEqual(self.user.databaseId, userResults.databaseId)
        self.assertEqual(self.user.name, userResults.name)