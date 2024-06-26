class Course:

    def __init__(self,supID,keywords, quota,realID=None,name=None):
        self._keywords = keywords
        self._supID = supID
        self._quota = quota
        self._realID = realID
        self._name = name

    def getcourseID(self):
        
        return self._supID

    def getKeywords(self):
        
        return self._keywords

    def getQuota(self):
        
        return self._quota

    def getcourseName(self):
        
        return self._name

    def getRealID(self):
        
        return self._realID

