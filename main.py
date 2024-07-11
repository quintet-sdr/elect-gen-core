import copy
import numpy as np
import random
import math
from json_util import readCoursesInfoJson, readStudentsInfoJson


def calculate_success_rate(num_students):
    if 0 <= num_students <= 16:
        return 0
    elif 17 <= num_students <= 20:
        return math.exp(num_students - 16)
    elif 21 <= num_students <= 28:
        return math.exp(4 - (num_students - 20))
    elif 29 <= num_students <= 34:
        return math.exp(num_students - 28)
    elif 35 <= num_students <= 40:
        return math.exp(6 - (num_students - 34))
    elif 41 <= num_students <= 56:
        return math.exp(num_students - 40)
    elif 57 <= num_students <= 72:
        return math.exp(16 - (num_students - 56))
    elif 73 <= num_students <= 88:
        return math.exp(num_students - 72)
    elif 89 <= num_students <= 104:
        return math.exp(16 - (num_students - 88))
    elif 105 <= num_students <= 120:
        return math.exp(num_students - 104)
    else:
        return 0


success_rate_dict = {i: calculate_success_rate(i) for i in range(0, 1000)}


def memoize(func):
    cache = dict()

    def memoized_func(*args):
        hashable_args = tuple(tuple(x) if isinstance(x, list) else x for x in args)
        if hashable_args in cache:
            return cache[hashable_args]
        result = func(*args)
        cache[hashable_args] = result
        return result

    return memoized_func


@memoize
def costFunction(students, courses):
    cost = 0
    student_priorities = np.array([student.finalPriority for student in students])
    student_GPAs = np.array([max(student.GPA, 0.1) for student in students])
    cost += np.sum((student_priorities ** 2) / student_GPAs)
    for course in courses:
        numOfStudents = len(course.students)
        cost += success_rate_dict[numOfStudents] ** 4
    return cost


def Distribute(students, courses):
    random.shuffle(students)
    students.sort(key=lambda student: student.GPA, reverse=True)
    for student in students:
        if not student.isDistributed:
            for courseName in student.availableCourses:
                for course in courses:
                    if courseName.lower() == course.name.lower() and course.quota > 0:
                        course.quota -= 1
                        course.students.append(student)
                        student.isDistributed = True
                        student.finalCourse = course.name
                        student.finalPriority = student.availableCourses.index(courseName) + 1
                        break
                if student.isDistributed:
                    break
    for student in students:
        if not student.isDistributed:
            other_courses = [course for course in courses if course.name not in student.availableCourses]
            other_courses.sort(key=lambda course: len(course.students))
            if other_courses:
                course = other_courses[0]
                course.students.append(student)
                student.isDistributed = True
                student.finalCourse = course.name
                student.finalPriority = len(student.availableCourses)
    cost = costFunction(students, courses)
    return students, cost


def improveDistribution(students, courses):
    noImprovements = 0
    cost = costFunction(students, courses)
    print("Initial cost: ", cost)
    while noImprovements < 1:
        newStudents = [copy.copy(s) for s in students]
        newCourses = [copy.copy(c) for c in courses]
        sortedStudents = sorted(students, key=lambda s: s.finalPriority, reverse=True)
        numStudents = max(int(len(students) * cost / 1000), 1)
        selectedStudents = sortedStudents[:numStudents]
        for student in selectedStudents:
            if student.finalPriority != 1 and student.finalPriority != 7:
                for findStudent in newStudents:
                    if findStudent.name == student.name:
                        findStudent.finalPriority = min(findStudent.finalPriority - 1,
                                                        len(findStudent.availableCourses) - 1)
                        if findStudent.finalPriority < len(findStudent.availableCourses):
                            findStudent.finalCourse = findStudent.availableCourses[findStudent.finalPriority]
                            findStudent.isDistributed = True
                            for course in newCourses:
                                if findStudent.availableCourses[findStudent.finalPriority] == course.name:
                                    course.quota -= 1
                                    course.students.append(student)
        Distribute(newStudents, newCourses)
        newCost = costFunction(newStudents, newCourses)

        if newCost < cost:
            print("Cost improved: ", newCost)
            cost = newCost
            students = newStudents
            courses = newCourses
            noImprovements = 0
        else:
            noImprovements += 1
            if noImprovements % 100 == 0:
                print("Without improvements: ", noImprovements)
    return students, cost


def startBasicAlgorithm(students_file_path, courses_file_path):
    print("Reading courses...")
    courses = readCoursesInfoJson(courses_file_path)
    print("Courses read")
    students = []
    print("Reading students...")
    readStudentsInfoJson(courses, students, students_file_path)
    print("Students read")
    print("Starting algorithm...")
    students_distributions = []
    costs = []
    for _ in range(20):
        students_copy = [copy.deepcopy(s) for s in students]
        courses_copy = [copy.deepcopy(c) for c in courses]
        students_copy, cost = Distribute(students_copy, courses_copy)
        students_copy, cost = improveDistribution(students_copy, courses_copy)
        students_distributions.append(students_copy)
        costs.append(cost)
    sorted_indices = np.argsort(costs)
    students_distributions = [students_distributions[i] for i in sorted_indices]
    costs = [costs[i] for i in sorted_indices]
    best_distribution_students = students_distributions[:20]
    best_distribution_cost = costs[:20]
    print("Algorithm finished")
    return best_distribution_students, best_distribution_cost
