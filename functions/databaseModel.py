from . import constants
from . import userModel
from . import statusHelper
import urllib.request
import json
import os


class Database(object):
    def __init__(self):
        self.database = {}
        for service in constants.WEBSITES:
            self.database[service] = []

    def setServiceusers(self, service, users):
        self.database[service] = users

    def userExists(self, userId, service):
        for user in self.database[service]:
            if user.id == userId:
                return True
        return False
    
    def getUserObj(self, userId, service):
        for service in self.database:
            for user in self.database[service]:
                if userId == user.id:
                    return user
        return None

    def getAllUserObjs(self):
        users = []
        for service in self.database:
            for user in self.database[service]:
                users.append(user)
        return users
    
    def writeDatabase(self):
        formattedDatabase = {}

        for service in self.database:
            userDict = {}
            for user in self.database[service]:
                userDict[user.id] = user.getAsJSON()
            formattedDatabase[service] = userDict

        json_object = json.dumps(formattedDatabase, indent=4)
        with open(constants.DATABASE_FILENAME, 'w') as outfile:
            outfile.write(json_object)

    def createUser(self, id, service, addButton):
        # get ids
        statusHelper.setuserOperationStatus("Got 0 user posts", "orange")

        request = "https://kemono.party/api/" + service.lower() + "/user/" + str(id) + "?o="
        i = 0
        knownIdList = []
        
        statusHelper.setuserOperationStatus("Looking for posts",  "orange")
        contents = urllib.request.urlopen(request + str(i)).read()
        response = json.loads(contents.decode())

        while(bool(response)): #keep running while contents exists
            statusHelper.setuserOperationStatus("Got " +str(i)+" user posts and looking more",  "orange")
            for obj in response:
                knownIdList.append(obj["id"])

            i += 50
            contents = urllib.request.urlopen(request + str(i)).read()
            response = json.loads(contents.decode())

        statusHelper.setuserOperationStatus("Finished getting all posts",  "orange")

        # actually write the new user and put it into the database
        self.database[service].append(userModel.User(id, service, checkedPostIds= knownIdList))
        self.writeDatabase()

        statusHelper.setuserOperationStatus("User is now in database",  "green")
        addButton["state"] = "normal"

    def knowUnknownPost(self, userId, service, postId):
        userObj = self.getUserObj(userId, service)
        userObj.checkedPostIds.append(postId)
        userObj.uncheckedPostIds.pop(postId)

    def getAllUnknownPosts(self):
        allUserObjs = self.getAllUserObjs()
        allUnknownPosts = []

        for user in allUserObjs:
            allUnknownPosts += user.uncheckedPostIds

        return allUnknownPosts
    
    def updateUserData(self, user, service, knownIds, unknownIds):
        obj = self.getUserObj(user,service)
        obj.checkedPostIds = knownIds
        obj.uncheckedPostIds = unknownIds 





def initalizeDatabase():
    # if database doesnt exist return a new database
    if(not os.path.isfile("./"+constants.DATABASE_FILENAME)):
        return Database()

    with open(constants.DATABASE_FILENAME, 'r') as openfile:
        return databaseJsonDecoder(json.load(openfile))


def databaseJsonDecoder(databaseDict):
    newDatabase = Database()

    for service in databaseDict:
        if service in newDatabase.database:
            usersList = []
            for userId in databaseDict[service]:
                user = userModel.User(userId, service, **databaseDict[service][userId])
                usersList.append(user)
            newDatabase.setServiceusers(service, usersList)

    return newDatabase