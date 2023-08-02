from . import databaseHelper
import threading
import urllib.request
import json

newPostsListVar = None 
getUpdateStatus = None
updatePostsButton = None

def passVars(newPostsListVarIn, getUpdateStatusIn, updatePostsButtonIn):
    global newPostsListVar, getUpdateStatus, updatePostsButton

    newPostsListVar = newPostsListVarIn
    getUpdateStatus = getUpdateStatusIn
    updatePostsButton = updatePostsButtonIn

def getUnreadPosts():
    threading.Thread(target=getUnreadPostsThread).start()
def getUnreadPostsThread():
    updatePostsButton.config(state="disabled")
    unknownPosts = databaseHelper.getUnknownPosts()
    newPostsListVar.set(unknownPosts)
    getUpdateStatus.config(text="Got database unknown posts!", bg = "orange")

    ## here we would go fetch api, compare posts info, and then continue to update newPostsListVar
    updatePostsButton.config(state="normal")

    users = databaseHelper.getAllUsers()

    for service in users:
        serviceUsers = users[service]
        for user in serviceUsers:
            getUpdateStatus.config(text="Getting posts from "+service+" for id:"+user, bg = "orange")
            
            i=0
            request = "https://kemono.party/api/" + service.lower() + "/user/" + str(user) + "?o=" + str(i)
            idList = []
            
            # first call
            contents = urllib.request.urlopen(request + str(i)).read()
            response = json.loads(contents.decode())
            for obj in response:
                idList.append(obj["id"])

            existingIds = databaseHelper.getUserData(user, service)
            knownIds = existingIds["checkedPostIds"]
            unkownIds = existingIds["uncheckedPostIds"]
            
            unseenIds = []

            for id in idList:
                if(id not in knownIds and id not in unkownIds):
                    unseenIds.append(id) #ill assume that updates usually target first page, this can miss
                                            # updates to previous pages
            
            unseenIdsSize = len(unseenIds)
            if(unseenIdsSize != 0): # if we found some new stuff, check all pages until we no longer find new 
                while(bool(response)): #keep running while contents exists
                    for obj in response:
                        idList.append(obj["id"])

                    i += 50
                    contents = urllib.request.urlopen(request + str(i)).read()
                    response = json.loads(contents.decode())

                    for id in idList:
                        if(id not in knownIds and id not in unkownIds):
                            unseenIds.append(id)
                    
                    newUnseenIdsSize = len(unseenIds)
                    if(unseenIdsSize == newUnseenIdsSize): # if no change then finish
                        break
                    else:
                        unseenIdsSize = newUnseenIdsSize
    
    getUpdateStatus.config(text="Finished getting posts from web", bg = "green")