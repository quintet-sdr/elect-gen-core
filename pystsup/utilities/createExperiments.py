from .acmParser import getPath, parseFile
from .createRandomData import createRandomData
from pystsup.data import *
from pystsup.evolutionary import *

import os
import numpy as np
import glob
import gzip
import json
import random


def read_preference_tsv(path, student=True):
    topicNames, topicPaths, topicIDs, levels = parseFile("pystsup/test/acm.txt")
    f = open(path, "r")
    raw_data = []
    base = "student" if student else "course"
    for line in f:
        fields = [int(x) for x in line.split("\t")]
        identifier = base + str(fields[0])
        kw = {}
        for i in range(1, 6):
            kw[i] = getPath(topicIDs[fields[i] + 1], topicNames, topicPaths, topicIDs)
        raw_data.append((identifier, kw))
        print(identifier, kw)
    return raw_data


def createExperimentsFromRealData(maxStu, minStu, stepStu, maxSup, minSup, stepSup, scenarios, student_path,
                                  course_path, folder="real_experiments", quotaMin=1, quotaMax=1.20, quotaStep=0.05,
                                  c=0.5, n=5):
    if not os.path.exists(folder):
        os.mkdir(folder)
    filenames = []
    rankWeights = Solution.calcRankWeights(c=c, n=n)
    students_raw = read_preference_tsv(student_path)
    courses_raw = read_preference_tsv(course_path, student=False)
    for num_students in range(minStu, maxStu + 1, stepStu):
        for num_courses in range(minSup, maxSup + 1, stepSup):
            for total_quota in [int(num_students * i) for i in np.arange(quotaMin, quotaMax + 0.01, quotaStep)]:
                maxQuota = 10
                minQuota = 4
                while num_courses * minQuota > total_quota:
                    minQuota -= 1
                while num_courses * maxQuota < total_quota:
                    maxQuota += 1
                for num_scenarios in range(1, scenarios + 1):
                    filename = str(num_students) + "_" + str(num_courses) + "_" + str(total_quota) + "_" + str(
                        num_scenarios)
                    destinationPath = folder + "/" + filename
                    students, courses = createRandomData(num_courses, num_students, total_quota, level=3,
                                                         maxQuota=maxQuota, minQuota=minQuota)
                    random.shuffle(students_raw)
                    random.shuffle(courses_raw)
                    i = 0
                    for student in students:
                        students[student]._keywords = students_raw[i][1]
                        i = i + 1
                    i = 0
                    for course in courses:
                        courses[course]._keywords = courses_raw[i][1]
                        i = i + 1
                    fitnessCache = calcFitnessCache(students, courses, rankWeights)
                    filenames.append(destinationPath)
                    population = {}
                    for i in [128, 256, 512]:
                        population[str(i)] = initializePopulation(i, students, courses, rankWeights, fitnessCache)
                    createFile(destinationPath, students, courses, minQuota, maxQuota, total_quota, num_scenarios,
                               fitnessCache, population, rankWeights)
    return filenames


def createExperiments(maxStu, minStu, stepStu, maxSup, minSup, stepSup, scenarios, folder="experiments", quotaMin=1,
                      quotaMax=1.20, quotaStep=0.05, acmLevel=3, c=0.5, n=5):
    if not os.path.exists(folder):
        os.mkdir(folder)
    filenames = []
    rankWeights = Solution.calcRankWeights(c=c, n=n)
    for num_students in range(minStu, maxStu + 1, stepStu):
        for num_courses in range(minSup, maxSup + 1, stepSup):
            for total_quota in [int(num_students * i) for i in np.arange(quotaMin, quotaMax + 0.01, quotaStep)]:
                maxQuota = 10
                minQuota = 4
                while num_courses * minQuota > total_quota:
                    minQuota -= 1
                while num_courses * maxQuota < total_quota:
                    maxQuota += 1
                for num_scenarios in range(1, scenarios + 1):
                    filename = str(num_students) + "_" + str(num_courses) + "_" + str(total_quota) + "_" + str(
                        num_scenarios)

                    destinationPath = folder + "/" + filename

                    students, courses = createRandomData(num_courses, num_students, total_quota, level=acmLevel,
                                                         maxQuota=maxQuota, minQuota=minQuota)

                    fitnessCache = calcFitnessCache(students, courses, rankWeights)

                    filenames.append(destinationPath)
                    population = {}

                    for i in [128, 256, 512]:
                        population[str(i)] = initializePopulation(i, students, courses, rankWeights, fitnessCache)

                    createFile(destinationPath, students, courses, minQuota, maxQuota, total_quota, num_scenarios,
                               fitnessCache, population, rankWeights)

        return filenames


def createFile(filename, students, courses, minQuota, maxQuota, quotaSum, testCase, fitnessCache, population,
               rankWeights):
    filename += ".json.gz"

    data = {}
    data['numberOfStudents'] = len(students)
    data['numberOfcourses'] = len(courses)
    data['testCase'] = testCase
    data['quotaSum'] = quotaSum
    data['minQuota'] = minQuota
    data['maxQuota'] = maxQuota
    data['students'] = students  # serialize
    data['courses'] = courses  # serialize
    data['rankWeights'] = rankWeights
    data['fitnessCache'] = fitnessCache
    data['population'] = population  # contains sub solutions

    with gzip.GzipFile(filename, 'w') as f:
        json_str = json.dumps(data, default=lambda o: o.__dict__)
        json_bytes = json_str.encode('utf-8')
        f.write(json_bytes)


def saveExpResults(filename, data):
    filename += ".json.gz"

    with gzip.GzipFile(filename, 'w') as f:
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        f.write(json_bytes)


def readFile(filename):
    with gzip.GzipFile(filename, 'r') as f:

        json_bytes = f.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

    students = data['students']
    courses = data['courses']
    fitnessCache = data['fitnessCache']
    rankWeights = data['rankWeights']
    population = data['population']

    details = ['numberOfStudents', 'numberOfcourses', 'testCase', 'quotaSum', 'minQuota', 'maxQuota']
    expDetails = {k: data[k] for k in details}

    for stu in students:
        new = Student.__new__(Student)
        new.__dict__ = students[stu]
        students[stu] = new

    for sup in courses:
        new = course.__new__(course)
        new.__dict__ = courses[sup]
        courses[sup] = new

    for i in population:
        for j in range(int(i)):
            new = Solution.__new__(Solution)

            graph = BipartiteGraph.__new__(BipartiteGraph)
            graph.__dict__ = population[i][j]['_graph']
            population[i][j]['_graph'] = graph

            new.__dict__ = population[i][j]

            population[i][j] = new

    return students, courses, population, fitnessCache, rankWeights, expDetails


def parseConfigFile(filename):
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    gen = data['genLimit']
    popSize = data['populationSize']
    mutationProbability = data['mutationProbability']
    swapProbability = data['swapProbability']
    transferProbability = data['transferProbability']
    crossoverOp = strToOp(data['crossoverOp'], 'crossover')
    mutationOp = strToOp(data['mutationOp'], 'mutation')
    selectionOp = strToOp(data['selectionOp'], 'selection')

    return gen, popSize, crossoverOp, mutationOp, selectionOp, mutationProbability, swapProbability, transferProbability


def updateConfigFile(filename, genLimit, popSize, muProb, swapProb, transProb):
    f = open(filename, 'r')
    data = json.load(f)
    f.close()

    f = open(filename, 'w')
    data['genLimit'] = genLimit
    data['populationSize'] = popSize
    data['mutationProbability'] = muProb
    data['swapProbability'] = swapProb
    data['transferProbability'] = transProb

    json.dump(data, f, indent=4)
    f.close()


def strToOp(name, op):
    if op == 'mutation':

        operator = mutate

    elif op == 'crossover':

        if name == 'kPoint':

            operator = kPoint

        elif name == 'crossover':

            operator = crossover

        elif name == 'uniform':
            operator = uniform

        elif name == 'sp_crossover':
            operator = sp_crossover

        elif name == 'crossover6':
            operator = crossover6

    elif op == 'selection':

        if name == 'tournamentSelection':
            operator = tournamentSelection
        elif name == 'rouletteWheel':
            operator = rouletteWheel

    return operator


def calcFitnessCache(students, courses, rankWeights):
    fitnessCache = {}
    dummySolution = Solution()

    for sup in courses:
        courseKeywords = courses[sup].getKeywords()
        for stu in students:
            studentKeywords = students[stu].getKeywords()
            f_stu, f_sup = dummySolution.kw_similarity(studentKeywords, courseKeywords, rankWeights)
            fitnessCache[str((stu, sup))] = (f_stu, f_sup)

    return fitnessCache


def initializePopulation(size, students, courses, rankWeights, fitnessCache):
    population = []
    count = 0
    while count < size:
        new = Solution.generateRandomSolution(students, courses)
        new.calcFitness(students, courses, rankWeights, fitnessCache)
        population.append(new)
        count += 1

    return population
