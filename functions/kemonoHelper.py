
from . import databaseModel
import threading
import urllib.request
import json

newPostsListVar = None 
getUpdateStatus = None
updatePostsButton = None

database = None

def passVars(newPostsListVarIn, getUpdateStatusIn, updatePostsButtonIn, databaseIn):
    global newPostsListVar, getUpdateStatus, updatePostsButton, database

    newPostsListVar = newPostsListVarIn
    getUpdateStatus = getUpdateStatusIn
    updatePostsButton = updatePostsButtonIn
    database = databaseIn

def getUnreadPosts():
    threading.Thread(target=getUnreadPostsThread).start()
def getUnreadPostsThread():
    updatePostsButton.config(state="disabled")
    unknownPosts = database.getAllUnknownPosts()
    newPostsListVar.set(unknownPosts)
    getUpdateStatus.config(text="Got database unknown posts!", bg = "orange")

    ## here we would go fetch api, compare posts info, and then continue to update newPostsListVar
    updatePostsButton.config(state="normal")

    users = database.getAllUserObjs()

    for user in users:
        service = user.service
        userId = user.id
        getUpdateStatus.config(text="Getting posts from "+service+" for id:"+userId, bg = "orange")
        
        i=0
        request = "https://kemono.party/api/" + service.lower() + "/user/" + str(userId) + "?o=" + str(i)
        idList = []
        
        # first call
        contents = urllib.request.urlopen(request + str(i)).read()
        response = json.loads(contents.decode())
        for obj in response:
            idList.append(obj["id"])

        knownIds = user.checkedPostIds
        unknownIds = user.uncheckedPostIds
        
        unseenIds = []

        for id in idList:
            if(id not in knownIds and id not in unknownIds and id not in unseenIds):
                unseenIds.append(id) #ill assume that updates usually target first page, this can miss
                                        # updates to previous pages
        
        unseenIdsSize = len(unseenIds)
        if(unseenIdsSize != 0): # if we found some new stuff, check all pages until we no longer find new 
            while(bool(response)): #keep running while contents exists

                i += 50
                contents = urllib.request.urlopen(request + str(i)).read()
                response = json.loads(contents.decode())
                for obj in response:
                    idList.append(obj["id"])

                for id in idList:
                    if(id not in knownIds and id not in unknownIds and id not in unseenIds):
                        unseenIds.append(id)
                
                newUnseenIdsSize = len(unseenIds) - unseenIdsSize
                if(unseenIdsSize == newUnseenIdsSize): # if no change then finish
                    break
                else:
                    unseenIdsSize = newUnseenIdsSize
        
        unknownIds = unknownIds + unseenIds
        database.updateUserData(userId, service, knownIds, unknownIds)
    
    unknownPosts = database.getAllUnknownPosts()
    newPostsListVar.set(unknownPosts)
    getUpdateStatus.config(text="Finished getting posts from web", bg = "green")