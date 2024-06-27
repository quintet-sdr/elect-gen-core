import random
from .acmParser import getPath, parseFile
from .integerPartition import partition
from pystsup.data import Student
from pystsup.data import course
import numpy


def createRandomData(m, n, quotaSum, level=3, maxQuota=10, minQuota=4, no_topics=5):
    topicNames, topicPaths, topicIDs, levels = parseFile("pystsup/test/acm.txt")

    numberOfcourses = m
    numberOfStudents = n

    courses = {}
    students = {}

    supId = "course"
    stuId = "student"

    quotas = partition(quotaSum, m, minQuota, maxQuota)

    topicsAvailable = [i for i in levels if levels[i] <= level]

    while m > 0:
        m -= 1
        toAdd = []
        sup_List = {}
        rank = 0

        for i in random.sample(topicsAvailable, no_topics):
            kw = topicIDs[i]
            rank += 1
            sup_List[rank] = [kw, getPath(kw, topicNames, topicPaths, topicIDs)]

        sup = supId + str(numberOfcourses - m)

        quota = random.choice(quotas)
        quotas.remove(quota)

        courseObject = course(sup, sup_List, quota)

        courses[sup] = courseObject

    while n > 0:
        n -= 1
        toAdd = []
        stu_List = {}
        rank = 0
        for i in random.sample(topicsAvailable, no_topics):
            kw = topicIDs[i]
            rank += 1
            stu_List[rank] = [kw, getPath(kw, topicNames, topicPaths, topicIDs)]

        stu = stuId + str(numberOfStudents - n)

        studentObject = Student(stu, stu_List)

        students[stu] = studentObject

    return students, courses


def createRandomDataExcel(m, n, quotaSum, level=3, maxQuota=10, minQuota=4, no_topics=5,
                          keywordsFile="pystsup/test/acm.txt"):
    topicNames, topicPaths, topicIDs, levels = parseFile(keywordsFile)

    numberOfcourses = m
    numberOfStudents = n

    courses = []
    students = []

    suprealID = "aab"

    quotas = partition(quotaSum, m, minQuota, maxQuota)

    f = open('random_names.txt', 'r').read()
    names = f.split("\n")

    topicsAvailable = [i for i in levels if levels[i] <= level]

    while m > 0:
        m -= 1

        realID = suprealID + str(random.randint(2333, 9999))
        name = random.choice(names)
        quota = random.choice(quotas)
        quotas.remove(quota)

        toAdd = [realID, name, quota]

        for i in random.sample(topicsAvailable, no_topics):
            kw = topicIDs[i]
            toAdd.append(kw.upper())

        courses.append(tuple(toAdd))

    while n > 0:
        n -= 1

        realID = str(random.randint(1000000, 9999999))
        name = random.choice(names)
        toAdd = [realID, name]

        for i in random.sample(topicsAvailable, no_topics):
            kw = topicIDs[i]

            toAdd.append(kw.upper())

        students.append(tuple(toAdd))

    return students, courses
