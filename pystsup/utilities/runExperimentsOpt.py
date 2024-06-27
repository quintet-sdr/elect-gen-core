from .createExperiments import readFile, strToOp
from pystsup.data import *
from pystsup.evolutionary import *
import sys
import numpy as np
import os
import glob
import json
import math
from pyomo.environ import *
from pyomo.opt import SolverFactory


def parseExpConfig(filename):
    f = open(filename, 'r')
    data = json.load(f)
    f.close()

    return data


def toString(identifier, testname, metricData):
    seq = [metricData['initial_maxFst'], metricData['initial_minFst'], metricData['initial_maxFsup'],
           metricData['initial_minFsup'], metricData['final_maxFst'], metricData['final_minFst'],
           metricData['final_maxFsup'], metricData['final_minFsup']]

    seq2 = [metricData['diversity'], metricData['numberOfGenerations'], metricData['total_time_generations'],
            metricData['avg_time_generation']]

    seq.extend(seq2)

    points = list(map(str, metricData['non_dominated_solutions']))

    point_evolution = str(metricData['evolution'])

    data = list(map(str, seq))

    result = identifier + testname + "\t" + "\t".join(data)

    result += "\t" + ",".join(points) + "\t" + point_evolution

    return result


def getExperimentFiles(foldername):
    path = foldername + "/" + "*.gz"
    filenames = glob.glob(path)
    return filenames


def saveResults(results, filename):
    filename += ".tsv"

    f = open(filename, 'a')

    for line in results:
        f.write(line + "\n")

    f.close()


def writeResult(result, filename, mode='a'):
    filename += ".tsv"

    f = open(filename, mode)

    f.write(result + "\n")
    f.close()


def createGAMSFileSup(filename, output, maxVersion=True):
    students, courses, populations, fitnessCache, rankWeights, expDetails = readFile(filename)

    f = open(output, "w")
    f.write("$offdigit\n")
    f.write("Sets\n")
    f.write("\ti\tstudents\t/ ")
    l_students = ",".join(list(students.keys()))
    f.write(l_students + "/\n")
    f.write("\tj\tcourses\t/ ")
    l_courses = ",".join(list(courses.keys()))
    f.write(l_courses + "/;\n")

    f.write("Parameters\n")
    f.write("c(j)\tcapacity of course\n")
    f.write("\t/ ")
    for course in courses:
        f.write("\t" + str(course) + "\t" + str(courses[course].getQuota()) + "\n")
    f.write(" / ;\n")

    f.write("Table v(i,j) valuation of being assigned i to j\n")
    f.write("$onDelim\n")
    f.write(",")
    l_courses = ",".join(list(courses.keys()))
    f.write(l_courses + "\n")
    for student in students:
        f.write(str(student))
        for course in courses:
            f.write("," + str(fitnessCache[str((student, course))][1]))
        f.write("\n")
    f.write("$offDelim\n")
    f.write(";\n")

    f.write("Scalar n_students number of students /" + str(len(students)) + "/;\n")
    f.write("Scalar n_courses number of courses /" + str(len(courses)) + "/;\n")

    f.write("Variables\n")
    f.write("\tx(i,j) if student is assigned to course \n")
    f.write("\tq(j) quality of allocation to course j \n")
    f.write("\twl(j) workload of allocation for course j\n")
    f.write("avg_wl average workload of allocation\n")
    f.write("\tz total quality of matching ;\n")
    f.write("Binary variables x ;\n")

    f.write("Equations\n")
    f.write("\tquality\tdefine objective function\n")
    f.write("\tworkload(j) workload of allocation for course j\n")
    f.write("average_workload average workload of allocation\n")
    f.write("\tsup_quality(j)   quality of matching for course j\n")
    f.write("\tmin_sup(j) minimum supervision quota for course j\n")
    f.write("\tmax_sup(j) maximum supervision quota for course j\n")
    f.write("\tstu_alloc(i) ensures that the student is allocated to someone ;\n")

    f.write("sup_quality(j) ..\t q(j) =e= sum(i, v(i,j)*x(i,j))/sum(i,x(i,j)) ;\n")
    f.write("workload(j) ..\t wl(j) =e= sum(i,x(i,j))/c(j) ;\n")
    f.write("average_workload ..\t avg_wl =e= (1/n_courses) * sum(j,wl(j)) ;\n")
    f.write(
        "quality ..\t z =e= (1/ (1+sqrt((1/n_courses) * sum(j, power(avg_wl-wl(j),2) )))**2 ) *  (1/n_courses) * sum(j,q(j)) ;\n")
    f.write("min_sup(j) .. sum(i, x(i,j)) =G= 1 ;\n")
    f.write("max_sup(j) .. sum(i, x(i,j)) =L= c(j) ;\n")
    f.write("stu_alloc(i) .. sum(j,x(i,j)) =e= 1 ;\n")
    f.write("Model project_alloc /all/ ;\n")

    rsol = Solution.generateRandomSolution(students, courses)
    g = rsol.getGraph()

    for student in students:
        for course in courses:
            if g.isEdge(course, student):
                f.write("x.L(\"" + str(student) + "\",\"" + str(course) + "\") = 1;\n");
            else:
                f.write("x.L(\"" + str(student) + "\",\"" + str(course) + "\") = 0;\n");

    f.write("Solve project_alloc using MINLP maximizing z ;")

    f.close()
    return students, courses, populations, fitnessCache, rankWeights, expDetails


def runExperimentsOpt(filename, studentVersion=True, maxVersion=True):
    students, courses, populations, fitnessCache, rankWeights, expDetails = readFile(filename)

    model = ConcreteModel()

    n_stu = len(students)
    n_sup = len(courses)

    model.students = Set(initialize=[student for student in students], doc="Student population")
    model.courses = Set(initialize=[course for course in courses], doc="course population")

    model.capacity = Param(model.courses, initialize={s: courses[s].getQuota() for s in courses}, doc="course quotas")

    idx_valuation = 0 if studentVersion else 1
    valuations = {}

    for student in students:
        for course in courses:
            valuations[(student, course)] = fitnessCache[str((student, course))][idx_valuation]

    model.valuations = Param(model.students, model.courses, initialize=valuations, doc="Values given to being assigned")

    model.n_students = Param(initialize=n_stu)
    model.n_courses = Param(initialize=n_sup)

    model.x = Var(model.students, model.courses, domain=Boolean, doc="Variables")

    def student_constraint(model, st):
        return sum(model.x[st, j] for j in model.courses) == 1

    def minimum_quota(model, sup):
        return sum(model.x[i, sup] for i in model.students) >= 1

    def maximum_quota(model, sup):
        return sum(model.x[i, sup] for i in model.students) <= model.capacity[sup]

    model.student_c = Constraint(model.students, rule=student_constraint,
                                 doc="Student constraints, so that they are supervised by only one")
    model.sup_min_c = Constraint(model.courses, rule=minimum_quota, doc="Minimum quota constraint")
    model.sup_max_c = Constraint(model.courses, rule=maximum_quota, doc="Maximum quota constraint")

    if studentVersion:
        def objective_rule(model):
            return sum([1 / model.n_students * model.valuations[i, j] * model.x[i, j] for i in model.students for j in
                        model.courses])
    else:
        def objective_rule(model):
            e = None
            for course in model.courses:
                s = sum([1 / model.n_courses * model.valuations[i, course] * model.x[i, course] for i in
                         model.students]) / sum(model.x[i, course] for i in model.students)
                if e is None:
                    e = s
                else:
                    e = e + s
            wl = None
            for course in model.courses:
                w = sum(model.x[i, course] for i in model.students) / model.capacity[course]
                if wl is None:
                    wl = w
                else:
                    wl = wl + w
            avg_wl = wl * 1 / model.n_courses
            penalization = None
            for course in model.courses:
                p = (sum(model.x[i, course] for i in model.students) / model.capacity[course] - avg_wl) * (
                            sum(model.x[i, course] for i in model.students) / model.capacity[course] - avg_wl)
                penalization = p if penalization is None else penalization + p
            penalization = sqrt(penalization / model.n_courses)
            # return e * 1/(1 + penalization)**2
            return e / (1 + penalization) ** 2
    model.objective = Objective(rule=objective_rule, sense=maximize if maxVersion else minimize,
                                doc="Objective function")

    # Setting initial solution
    rsol = Solution.generateRandomSolution(students, courses)
    g = rsol.getGraph()

    for student in students:
        for course in courses:
            if g.isEdge(course, student):
                model.x[student, course].set_value(1)
            else:
                model.x[student, course].set_value(0)

    rsol.calcFitness(students, courses, rankWeights, fitnessCache)

    opt = None
    if studentVersion:
        opt = SolverFactory("glpk")
    else:
        opt = SolverFactory("couenne")

    result = opt.solve(model)

    return expDetails, result["Problem"][0]["Lower bound"], result["Problem"][0]["Upper bound"]


def runAllExperimentsOptStudent(foldername):
    print("numberOfStudents\tnumberOfcourses\tquotaSum\ttestCase\tlowerBound\tupperBound")
    filenames = getExperimentFiles(foldername)

    for name in filenames:
        expDetails, aux, ub = runExperimentsOpt(name)
        expDetails, lb, aux = runExperimentsOpt(name, maxVersion=False)
        print(str(expDetails["numberOfStudents"]) + "\t" + str(expDetails["numberOfcourses"]) + "\t" + str(
            expDetails["quotaSum"]) +
              "\t" + str(expDetails["testCase"]) + "\t" + str(lb) + "\t" + str(ub))
