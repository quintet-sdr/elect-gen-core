class Student:

    def __init__(self, stuID, keywords, realID=None, name=None):
        self._keywords = keywords
        self._stuID = stuID
        self._realID = realID
        self._name = name

    def getStudentID(self):
        return self._stuID

    def getStudentName(self):
        return self._name

    def getRealID(self):
        return self._realID

    def getKeywords(self):
        return self._keywords
