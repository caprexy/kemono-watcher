from inputPanel import statusHelper
import threading
import urllib.request
import json

newPostsListVar = None 
updatePostsButton = None

database = None

def passVars(newPostsListVarIn, updatePostsButtonIn, databaseIn):
    global newPostsListVar, updatePostsButton, database

    newPostsListVar = newPostsListVarIn
    updatePostsButton = updatePostsButtonIn
    database = databaseIn

def getUnreadPosts():
    threading.Thread(target=getUnreadPostsThread).start()
def getUnreadPostsThread():
    updatePostsButton.config(state="disabled")
    unknownPosts = database.getAllUnknownPostsIdandService()
    newPostsListVar.set(unknownPosts)
    statusHelper.setGetUpdatesStatusLabelValues("Got database unknown posts!", "orange")

    ## here we would go fetch api, compare posts info, and then continue to update newPostsListVar
    updatePostsButton.config(state="normal")

    users = database.getAllUsersObj()

    for user in users:
        service = user.service
        userId = str(user.id)
        statusHelper.setGetUpdatesStatusLabelValues("Getting posts from "+service+" for id:"+userId, "orange")
        
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
    
    unknownPosts = database.getAllUnknownPostsIdandService()
    newPostsListVar.set(unknownPosts)
    statusHelper.setGetUpdatesStatusLabelValues("Finished getting posts from web", "green")