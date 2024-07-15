"""Core algorithm for distributing students to courses.
"""

import copy
import numpy as np
import random
from json_util import readCoursesInfoJson, readStudentsInfoJson

success_rate_dict = {}
courses_rate_dict = {}


def get_course_rate(x, a, c, d, e, limit, lostPerCycle=0.1):
    """Calculates the success rate based on the number of students in a course
    :param x: number of students in the course
    :param a: lower bound for the whole course
    :param c: lower bound for the optimal one group
    :param d: upper bound for the optimal one group
    :param e: upper bound for the one group
    :param limit: upper bound for the whole course
    :param lostPerCycle: lost coefficient per cycle
    :return: success rate
    """

    cycleMultiplier = 1 - lostPerCycle * (x // e)
    b = (a + c) * 0.5
    if x > limit:
        return 0
    if x // e == 0:
        if x < a:
            return 0
        if x < b:
            y1 = 0
            y2 = cycleMultiplier * 7 / 8
            x1 = a
            x2 = b
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b
        if x < c:
            y1 = cycleMultiplier * 7 / 8
            y2 = cycleMultiplier
            x1 = b
            x2 = c
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b
        if x < d:
            return cycleMultiplier
        if x < e:
            y1 = cycleMultiplier
            y2 = cycleMultiplier / 2
            x1 = d
            x2 = e
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b
    else:
        x = x % e
        if x < a / 2:
            return cycleMultiplier / 2
        if x < b:
            y1 = cycleMultiplier / 2
            y2 = cycleMultiplier * 19 / 20
            x1 = a / 2
            x2 = b
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b
        if x < c:
            y1 = cycleMultiplier * 19 / 20
            y2 = cycleMultiplier
            x1 = b
            x2 = c
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b
        if x < d:
            return cycleMultiplier
        if x < e:
            y1 = cycleMultiplier
            y2 = cycleMultiplier / 2
            x1 = d
            x2 = e
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            return k * x + b


def course_success_rate(num_students, a, b, c, d, limit):
    """Calculates the success rate based on the number of students in a course
    :param num_students: number of students in the course
    :param a: lower bound for the first piecewise function
    :param b: upper bound for the first piecewise function
    :param c: lower bound for the second piecewise function
    :param d: upper bound for the second piecewise function
    :param limit: limit for the number of students
    :return: success rate
    """

    if num_students == 0:
        return -0.15
    elif num_students < limit:
        return -get_course_rate(num_students, a, b, c, d, limit)
    else:
        return 0


def memoize(func):
    """Memoization decorator for the cost function
    :param func: cost function
    :return: memoized function
    """

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
    """Cost function for the algorithm
    :param students: list of Student objects
    :param courses: list of Course objects
    :return: cost
    """

    cost = 0
    student_priorities = np.array([student.finalPriority for student in students])
    student_GPAs = np.array([max(student.GPA, 0.1) for student in students])
    cost += np.sum((student_priorities ** 3) / student_GPAs * 6)
    for course in courses:
        numOfStudents = len(course.students)
        course_rate = courses_rate_dict[course.name]
        cost += course_rate[numOfStudents] * len(students)
    return cost


def Distribute(students, courses):
    """Distributes students to courses
    :param students: list of Student objects
    :param courses: list of Course objects
    :return: distributed students and cost
    """

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
                course.quota -= 1
                student.finalPriority = len(student.availableCourses)
    cost = costFunction(students, courses)
    return students, cost


def improveDistribution(students, courses):
    """Improves the distribution of students to courses
    :param students: list of Student objects
    :param courses: list of Course objects
    :return: improved students and cost
    """

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


def max_qouta_course(courses):
    """Returns the course with the maximum quota
    :param courses: list of Course objects
    :return: course with the maximum quota
    """

    max_quota = 0
    max_quota_course = None
    for course in courses:
        if course.quota > max_quota:
            max_quota = course.quota
            max_quota_course = course
    return max_quota_course


def startBasicAlgorithm(students_file_path, courses_file_path):
    global success_rate_dict
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
    max_quota = max_qouta_course(courses).quota + 1
    print("Max quota: ", max_quota)
    for i in courses:
        x_values = [x for x in range(len(students))]
        y_values = [course_success_rate(x, 10, 22, 28, 40, max_quota) for x in x_values]
        courses_rate_dict[i.name] = {x: y for x, y in zip(x_values, y_values)}
    print(courses_rate_dict)
    for _ in range(10):
        students_copy = [copy.deepcopy(s) for s in students]
        courses_copy = [copy.deepcopy(c) for c in courses]
        students_copy, cost = Distribute(students_copy, courses_copy)
        students_copy, cost = improveDistribution(students_copy, courses_copy)
        students_distributions.append(students_copy)
        costs.append(cost)
    sorted_indices = np.argsort(costs)
    students_distributions = [students_distributions[i] for i in sorted_indices]
    costs = [costs[i] for i in sorted_indices]
    best_distribution_students = students_distributions[:10]
    best_distribution_cost = costs[:10]
    print("Algorithm finished")
    return best_distribution_students, best_distribution_cost, courses_rate_dict
