import json
import os
import urllib.request
from . import constants

database = None
addUserResultEle = None
addButtonutton = None

# database management
def initalizeDatabase():
    global database
    # check if database exists, if it doesn't then initalize it
    if(not os.path.isfile("./"+constants.DATABASE_FILENAME)):
        # build first database
        database = {}
        for website in constants.WEBSITES:
            database[website] = {}

        json_object = json.dumps(database, indent=4)
        with open(constants.DATABASE_FILENAME, 'w') as outfile:
            outfile.write(json_object)
    else: # if it does then load it
        with open(constants.DATABASE_FILENAME, 'r') as openfile:
            database = json.load(openfile)

def userExists(userId, service):
    return userId in database[service]

def writeUser(userId, service):
    global database, addButtonutton

    # get ids
    addUserResultEle.config(text="Got 0 user posts", bg = "orange")

    request = "https://kemono.party/api/" + service.lower() + "/user/" + str(userId) + "?o="
    i = 0
    idList = []
    
    # first call
    contents = urllib.request.urlopen(request + str(i)).read()
    response = json.loads(contents.decode())

    while(bool(response)): #keep running while contents exists
        for obj in response:
            idList.append(obj["id"])

        i += 50
        addUserResultEle.config(text="Got " +str(i)+" user posts", bg = "orange")
        contents = urllib.request.urlopen(request + str(i)).read()
        response = json.loads(contents.decode())
        

    addUserResultEle.config(text="Finished getting all posts", bg = "orange")

    if(len(idList) == 0):
        addUserResultEle.config(text="Didnt find any posts so didnt save!", bg = "orange")
        return
    # actually write the new user and put it into the database
    database[service][userId] = {"checkedPostIds":idList,
                                 "uncheckedPostIds":[],
                                 }
    addUserResultEle.config(text="User is now in database", bg = "green")
    writeDatabase()

    addButtonutton["state"] = "normal"

def getUserData(userId, service):
    try:
        return database[service][userId]
    except:
        return []

def updateUserData(userId, service, knownList, unknownList):
    
    data = {"checkedPostIds":knownList,
            "uncheckedPostIds":unknownList}
    
    database[service][userId] = data
    writeDatabase()

def deleteUserData(userId, service):

    del database[service][userId]
    writeDatabase()

def writeDatabase():
    global database
    json_object = json.dumps(database, indent=4)
    with open(constants.DATABASE_FILENAME, 'w') as outfile:
        outfile.write(json_object)

def getUnknownPosts():
    unknownPosts = []
    for service in database:
        for user in database[service]:
            for unknownPostId in database[service][user]["uncheckedPostIds"]:
                unknownPosts.append(user+","+service+","+unknownPostId)
    
    return unknownPosts

def getAllUsers():
    global database
    users = {}
    for service in database:
        serviceUsers = []
        for user in database[service]:
            serviceUsers.append(user)
        users[service] = serviceUsers

    return users

def knowUnknownPost(user, service, post):

    knownList = database[service][user]["checkedPostIds"]
    knownList.append(post)
    knownList.sort()
    knownList.reverse()
    
    unknownList = database[service][user]["uncheckedPostIds"]
    unknownList.remove(post)
    unknownList.sort()
    unknownList.reverse()

    writeDatabase()
