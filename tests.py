import copy
import unittest
import os
from main import Distribute, costFunction, startBasicAlgorithm, improveDistribution
from models import Student, Course
from excel_util import writeResults
from json_util import readCoursesInfoJson, readStudentsInfoJson


class TestStudentCourseAllocation(unittest.TestCase):
    def setUp(self):
        self.courses_json_file = 'courses.json'
        self.students_json_file = 'students.json'
        self.courses = readCoursesInfoJson(self.courses_json_file)
        self.students = []
        readStudentsInfoJson(self.courses, self.students, self.students_json_file)
        self.errorCourse = Course(-1, "ERROR", 0)

    def test_readCoursesInfo(self):
        self.assertIsInstance(self.courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in self.courses))

    def test_readStudentsInfo(self):
        self.assertIsInstance(self.students, list)
        self.assertTrue(all(isinstance(student, Student) for student in self.students))

    def test_student_finalPriority(self):
        startBasicAlgorithm(self.students_json_file, self.courses_json_file)
        self.assertTrue(all(1 <= student.finalPriority <= 7 for student in self.students))

    def test_costFunction(self):
        startBasicAlgorithm(self.students_json_file, self.courses_json_file)
        cost = costFunction(self.students, self.courses)
        self.assertIsInstance(cost, float)

    def test_improveDistribution(self):
        students_copy = [copy.deepcopy(s) for s in self.students]
        courses_copy = [copy.deepcopy(c) for c in self.courses]
        students_copy, initial_cost = Distribute(students_copy, courses_copy)
        improved_students, improved_cost = improveDistribution(students_copy, courses_copy)
        self.assertLessEqual(improved_cost, initial_cost)
        self.assertTrue(all(student.isDistributed for student in improved_students))
        self.assertIsInstance(improved_cost, float)

    def test_writeResults(self):
        best_distributions, best_distribution_costs, courses_rate_dict = startBasicAlgorithm(self.students_json_file,
                                                                                             self.courses_json_file)
        writeResults(best_distributions, best_distribution_costs, self.courses, courses_rate_dict)
        self.assertTrue(os.path.exists('Results.xlsx'))


if __name__ == '__main__':
    unittest.main()
