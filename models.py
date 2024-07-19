"""Student and Course classes"""


class Student:

    def __init__(self, email, gpa, keywords, availableCourses):
        self.isDistributed = False
        self.email = email
        self.gpa = gpa
        self.keywords = keywords
        self.finalCourse = ""
        self.finalPriority = 6
        self.availableCourses = availableCourses



class Course:

    def __init__(self, codename, min_overall, max_overall, low_in_group, high_in_group, max_in_group):
        self.codename = codename
        self.min_overall = min_overall
        self.max_overall = max_overall
        self.low_in_group = low_in_group
        self.high_in_group = high_in_group
        self.max_in_group = max_in_group
        self.students = []
