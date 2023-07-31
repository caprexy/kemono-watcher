import json
import os
import urllib.request
from . import constants

databaseFileName = "database.json"
database = None
addUserResultEle = None
addButtonutton = None

# database management
def initalizeDatabase(addUserResultEleIn, addButtonuttonIn):
    global database, addUserResultEle, addButtonutton

    addUserResultEle = addUserResultEleIn
    addButtonutton = addButtonuttonIn

    # check if database exists, if it doesn't then initalize it
    if(not os.path.isfile("./"+databaseFileName)):
        # build first database
        database = {}
        for website in constants.WEBSITES:
            database[website] = {}

        json_object = json.dumps(database, indent=4)
        with open(databaseFileName, 'w') as outfile:
            outfile.write(json_object)
    else: # if it does then load it
        with open(databaseFileName, 'r') as openfile:
            database = json.load(openfile)

def userExists(userId, service):
    global database
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
        

    addButtonutton["state"] = "normal"
    addUserResultEle.config(text="Finished getting all posts", bg = "orange")


    # actually write the new user and put it into the database
    database[service][userId] = {"checkedPostIds":idList}

    addUserResultEle.config(text="User is now in database", bg = "green")
    writeDatabase()


def writeDatabase():
    global database
    json_object = json.dumps(database, indent=4)
    with open(databaseFileName, 'w') as outfile:
        outfile.write(json_object)