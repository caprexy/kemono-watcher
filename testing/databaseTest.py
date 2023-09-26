import unittest
import sys
import os

sys.path.append('../')

import models.databaseModel as database
import constants

class databaseTests(unittest.TestCase):
        
    def setUp(self):
        self.database = database.Database()

    def tearDown(self):
        self.database.close()
        if os.path.exists(constants.DATABASE_FILENAME):
            os.remove(constants.DATABASE_FILENAME)

    def testDatabaseSetup(self):
        print("a")