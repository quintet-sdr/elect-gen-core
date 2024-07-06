import unittest
import os
from main import Student, Course, readCoursesInfo, readStudentsInfo, Distribute, costFunction, writeResults


class TestStudentCourseAllocation(unittest.TestCase):
    def setUp(self):
        self.courses = readCoursesInfo()
        self.students = readStudentsInfo(self.courses)
        self.errorCourse = Course(-1, "ERROR", 0)

    def test_readCoursesInfo(self):
        self.assertIsInstance(self.courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in self.courses))

    def test_readStudentsInfo(self):
        self.assertIsInstance(self.students, list)
        self.assertTrue(all(isinstance(student, Student) for student in self.students))

    def test_writeResults(self):
        writeResults(self.students)
        self.assertTrue(os.path.exists('Results.xlsx'))

    def test_costFunction(self):
        Distribute(self.students, self.errorCourse)
        cost = costFunction(self.students)
        self.assertIsInstance(cost, float)

    def test_student_finalPriority(self):
        Distribute(self.students, self.errorCourse)
        self.assertTrue(all(1 <= student.finalPriority <= 7 for student in self.students))


if __name__ == '__main__':
    unittest.main()
