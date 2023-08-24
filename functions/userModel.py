
class User(object):
    def __init__(self, id, service, checkedPostIds=[], uncheckedPostIds=[]):
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