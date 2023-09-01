import json

class User(object):
    def __init__(self, databaseId, name, id, service, checkedPostIds=[], uncheckedPostIds=[]):
        self.databaseId = databaseId
        self.name = name
        self.id = id
        self.service = service
        self.checkedPostIds = checkedPostIds
        self.uncheckedPostIds = uncheckedPostIds

    def __str__(self):
        return f"User {self.id} of service {self.service}"
    
    def __repr__(self):
        return f"User {self.id} of service {self.service}"
    
    def getAsJSON(self):
        return {
            "checkedPostIds" : self.checkedPostIds,
            "uncheckedPostIds" : self.uncheckedPostIds
        }
    
    def getAsRowTuple(self):
        return (self.databaseId, self.name, self.id, self.service, json.dumps(self.checkedPostIds), json.dumps(self.uncheckedPostIds))

def convertRowIntoUser(rowTuple):
    databaseId = rowTuple[0]
    name = rowTuple[1]
    id = rowTuple[2]
    service = rowTuple[3]
    checkedPostIds = json.loads(rowTuple[4])
    uncheckedPostIds = json.loads(rowTuple[5])
    return User(databaseId, name, id, service, checkedPostIds, uncheckedPostIds)