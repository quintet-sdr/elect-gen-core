from openpyxl import load_workbook
import xlwt
import random
import copy


class Student:
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
    def __init__(self, ID, name, quota):
        self.ID = ID
        self.name = name
        self.quota = quota
        self.students = []


def readCoursesInfo():
    courseFile = 'Courses table.xlsx'
    courseWB = load_workbook(courseFile)
    courseSheet = courseWB[courseWB.sheetnames[0]]
    courses = []
    for i in range(2, courseSheet.max_row + 1):
        ID = courseSheet.cell(row=i, column=1).value
        name = courseSheet.cell(row=i, column=2).value
        quota = courseSheet.cell(row=i, column=3).value
        courses.append(Course(ID, name, quota))
    return courses


def readStudentsInfo(courses):
    studentFile = 'Students table.xlsx'
    studentWB = load_workbook(studentFile)
    studentSheet = studentWB[studentWB.sheetnames[0]]
    students = []
    for i in range(2, studentSheet.max_row + 1):
        ID = studentSheet.cell(row=i, column=1).value
        name = studentSheet.cell(row=i, column=2).value
        GPA = studentSheet.cell(row=i, column=3).value
        keywords = []
        availableCourses = []
        for j in range(4, 9):
            keyword = studentSheet.cell(row=i, column=j).value
            flag = False
            for course in courses:
                if course.name.lower() == keyword.lower():
                    flag = True
                    keywords.append(course)
                    if course.ID != -1:
                        availableCourses.append(course)
                    break
            if not flag:
                course = Course(-1, keyword, 0)
                courses.append(course)
                keywords.append(course)
        GPA = float(GPA)
        students.append(Student(ID, name, GPA, keywords, availableCourses))
    students.sort(key=lambda student: student.GPA, reverse=True)
    return students


def writeResults(students):
    results = xlwt.Workbook(encoding="utf-8")
    resultsSheetResults = results.add_sheet("Results")
    resultsSheetResults.write(0, 0, "Student ID")
    resultsSheetResults.write(0, 1, "Student Name")
    resultsSheetResults.write(0, 2, "Final priority")
    resultsSheetResults.write(0, 3, "Course Name")
    resultsSheetResults.write(0, 5, "1 priority")
    resultsSheetResults.write(0, 6, "2 priority")
    resultsSheetResults.write(0, 7, "3 priority")
    resultsSheetResults.write(0, 8, "4 priority")
    resultsSheetResults.write(0, 9, "5 priority")
    resultsSheetResults.write(0, 10, "No priority")
    resultsSheetResults.write(0, 11, "Bad input")
    totalResults = [0] * 7
    i = 0
    for student in students:
        i += 1
        resultsSheetResults.write(i, 0, student.ID)
        resultsSheetResults.write(i, 1, student.name)
        resultsSheetResults.write(i, 2, student.finalPriority)
        resultsSheetResults.write(i, 3, student.finalCourse)
        totalResults[student.finalPriority - 1] += 1
    for j in range(0, 7):
        resultsSheetResults.write(1, j + 5, totalResults[j])
    results.save("Results.xlsx")


def costFunction(students):
    cost = 0
    for student in students:
        if student.finalPriority == 7 or student.GPA == 0:
            continue
        cost += (student.finalPriority ** 2) / student.GPA
    return cost


def Distribute(students, errorCourse):
    # Initial student's distribution
    for student in students:
        for course in student.keywords:
            if student.keywords.count(course) > 1:
                student.finalPriority = 7
                student.availableCourses = list(set(student.availableCourses))
                while len(student.keywords) < 5:
                    student.add = errorCourse
        if not student.isDistributed:
            for course in student.availableCourses:
                if course.quota > 0:
                    course.quota -= 1
                    course.students.append(student)
                    student.isDistributed = True
                    student.finalCourse = course.name
                    student.finalPriority = student.availableCourses.index(course) + 1
                    break

    # Trying to Distribute bad input
    for student in students:
        if not student.isDistributed:
            for course in student.availableCourses:
                if course.quota > 0:
                    course.quota -= 1
                    course.students.append(student)
                    student.isDistributed = True
                    student.finalCourse = course.name
                    student.finalPriority = student.availableCourses.index(course) + 1
                    break


courses = readCoursesInfo()
students = readStudentsInfo(courses)

clearCourses = copy.deepcopy(courses)
clearStudents = copy.deepcopy(students)

errorCourse = Course(-1, "ERROR", 0)

Distribute(students, errorCourse)

# Randomly scattering students and trying to improve the costFunction
noImprovements = 0
while noImprovements < 10000:
    cost = costFunction(students)
    newStudents = copy.deepcopy(clearStudents)
    newCourses = copy.deepcopy(clearCourses)
    randomStudents = random.sample(students, int(len(students) / 20))
    for student in randomStudents:
        if student.finalPriority != 1 and student.finalPriority != 7:
            for findStudent in newStudents:
                if findStudent.name == student.name:
                    findStudent = copy.deepcopy(student)
                    findStudent.finalPriority = min(findStudent.finalPriority - 1,
                                                    len(findStudent.availableCourses) - 1)
                    findStudent.finalCourse = findStudent.availableCourses[findStudent.finalPriority]
                    findStudent.isDistributed = True
    Distribute(newStudents, errorCourse)
    newCost = costFunction(newStudents)
    if newCost < cost:
        print("Cost difference: ", cost - newCost)
        cost = newCost
        students = copy.deepcopy(newStudents)
        courses = copy.deepcopy(newCourses)
        noImprovements = 0
    else:
        noImprovements += 1
        if noImprovements % 100 == 0:
            print("Without improvements: ", noImprovements)
writeResults(students)
