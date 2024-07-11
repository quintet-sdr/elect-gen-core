"""Student and Course classes"""


class Student:
    """Student class
    :param ID: student ID
    :param name: student name
    :param GPA: student GPA
    :param keywords: list of keywords
    :param availableCourses: list of available courses
    """

    def __init__(self, ID, name, GPA, keywords, availableCourses):
        self.isDistributed = False
        self.ID = ID
        self.name = name
        self.GPA = GPA
        self.keywords = keywords
        self.finalCourse = ""
        self.finalPriority = 6
        self.availableCourses = availableCourses


class Course:
    """Course class
    :param ID: course ID
    :param name: course name
    :param quota: course quota
    """

    def __init__(self, ID, name, quota):
        self.ID = ID
        self.name = name
        self.quota = quota
        self.students = []
