import numpy
from .bipartiteGraph import BipartiteGraph


class Solution:

    def __init__(self, graph=None):

        if graph:
            self._graph = graph
        else:
            self._graph = BipartiteGraph()

        # NSGA II

        self._Fsup = None
        self._Fst = None

        self.dominationCount = None
        self.dominatedSolution = None
        self.rank = None
        self.crowdingDistance = None

    def generateRandomSolution(students, courses):

        g = BipartiteGraph.createRandomGraph(students, courses)

        return Solution(graph=g)

    def getFst(self):
        return self._Fst

    def getFsup(self):

        return self._Fsup

    def setFst(self, Fst):

        self._Fst = Fst

    def setFsup(self, Fsup):

        self._Fsup = Fsup

    def dominates(self, solution2):

        # Getting the fitness values from both solutions

        sol1Fst = self._Fst
        sol1Fsup = self._Fsup

        sol2Fst = solution2.getFst()
        sol2Fsup = solution2.getFsup()

        # Condition 1 - When both points (Fst, Fsup) of this solution are strictly greater than solution2 points
        cond1 = (sol1Fst > sol2Fst) and (sol1Fsup > sol2Fsup)

        # Condition 2 - When Fst of this solution is greater than or equal to and Fsup is stricly greater than
        cond2 = (sol1Fst >= sol2Fst) and (sol1Fsup > sol2Fsup)

        # Condition 3 - When Fst of this solution is strictly greater than and Fsup is greater than or equal to
        cond3 = (sol1Fst > sol2Fst) and (sol1Fsup >= sol2Fsup)

        # If any of those conditions is true it means this solution dominates solution2

        if cond1 or cond2 or cond3:
            return True
        else:
            return False

    def __lt__(self, sol2):

        if isinstance(sol2, Solution):

            cond1 = self.rank < sol2.rank
            cond2 = (self.rank == sol2.rank) and (self.crowdingDistance > sol2.crowdingDistance)

            if cond1 or cond2:
                return True
            else:
                return False

    def __key(self):

        return self._graph

    def __hash__(self):

        return hash(self.__key())

    def __eq__(self, sol2):

        return (self._graph == sol2.getGraph())

    def calcRankWeights(c=0.5, n=5):

        rankWeights = {}
        summation = 0
        for i in range(n):
            temp = c ** i
            rankWeights[i + 1] = temp
            summation += temp
        for i in rankWeights:
            rankWeights[i] = rankWeights[i] / summation

        return rankWeights

    def _intersection(self, kw1, kw2):

        count = 0
        indices = (len(kw1) - 1, len(kw2) - 1)

        # Start checking from the end of the list until they keywords match

        while indices[0] >= 0 and indices[1] >= 0:
            if kw1[indices[0]] == kw2[indices[1]]:
                count += 1
                indices = (indices[0] - 1, indices[1] - 1)
            else:
                break

        return count

    def kw_similarity(self, studentKeywords, courseKeywords, rankWeights):

        studentKeywords_Size = len(studentKeywords)
        courseKeywords_Size = len(courseKeywords)

        result1 = 0  # fst
        result2 = 0  # fsup

        # Dictionary to keep track of the most similar keyword value and rank similarity values

        track = {}  # for course fitness
        track2 = {}  # for student fitness

        for sup_rank in courseKeywords:
            # index 0 - most similar keyword (course points) value
            # index 1 - rank similairty value for that 'most similar keyword'

            track[sup_rank] = [0, 0]

        for stu_rank in studentKeywords:
            # index 0 - rank similarity value for the most similar keyword

            track2[stu_rank] = 0

        for student_rank in studentKeywords:

            student_kw = studentKeywords[student_rank][0]
            student_path = studentKeywords[student_rank][1]

            curr_max1 = 0  # keeps track of the most similar keyword value for student

            for course_rank in courseKeywords:

                course_path = courseKeywords[course_rank][1]
                course_kw = courseKeywords[course_rank][0]

                common_keywords = self._intersection(student_path, course_path)

                if common_keywords != 0:

                    points1 = common_keywords / len(student_path)  # student points
                    points2 = common_keywords / len(course_path)  # course points

                    rank_Similarity = 1 / (1 + abs(student_rank - course_rank))

                    curr1 = points1
                    curr2 = points2

                    # if student points is greater than previous student points then update values

                    if curr1 > curr_max1:
                        curr_max1 = curr1
                        track2[student_rank] = rank_Similarity

                    # if course points is greater than previor course points then update values

                    if curr2 > track[course_rank][0]:
                        track[course_rank][0] = curr2
                        track[course_rank][1] = rank_Similarity

            # Sum the values for all the keywords of the student
            result1 += curr_max1 * track2[student_rank] * rankWeights[student_rank]

        # Sum the values for all the keywords of the course
        for i in track:
            if track[i] != 0:
                result2 += track[i][0] * track[i][1] * rankWeights[i]

        return result1, result2

    def getAverageStructuralFitness(self, courses):
        edges = self._graph.getEdges()
        workloads = []
        for sup in courses:
            quota = courses[sup].getQuota()
            students_allocated = edges[sup]
            workloads.append(len(students_allocated) / quota)
        wf = numpy.mean(workloads)
        return wf

    def getStructuralFitness(self, courses):
        edges = self._graph.getEdges()
        workloads = []
        for sup in courses:
            quota = courses[sup].getQuota()
            students_allocated = edges[sup]
            workloads.append(len(students_allocated) / quota)
        wf = numpy.std(workloads)
        return 1 / (1 + wf) ** 2

    def calcFitness(self, students, courses, rankWeights, fitnessCache):

        quotaSum = 0

        edges = self._graph.getEdges()

        fitnessSup_min = float("inf")
        fitnessSup_avg = 0
        n_sup = len(courses)
        n_stu = len(students)
        workloads = []

        fitness_st = float("inf")
        summation_Fst = 0

        for sup in edges:
            quota = courses[sup].getQuota()
            quotaSum += quota
            students_allocated = edges[sup]

            n = len(students_allocated)

            temp_total = 0

            workloads.append(n / quota)

            for stu in students_allocated:

                temp_Fst, temp_fsup = fitnessCache[str((stu, sup))]  # changed to str because of JSON file saving

                temp_total += temp_fsup

                summation_Fst += temp_Fst

                if temp_Fst < fitness_st:
                    fitness_st = temp_Fst

            average = temp_total / n  # For course Fitness

            if average < fitnessSup_min:
                fitnessSup_min = average
            fitnessSup_avg += average

        st = self.getStructuralFitness(courses)
        fitnessSup = (fitnessSup_avg / n_sup) * st
        if fitnessSup > 1.0:
            print(fitnessSupi, "ERROR")
            print(fitnessSup_avg, n_sup)
            assert fitnessSup <= 1.0

        self._Fst = summation_Fst / n_stu
        assert self._Fst < 1.0
        if self._Fst > 1.0:
            print("ERROR", self._Fst, summation_Fst, n_stu)
            assert self._Fst <= 1.0
        self._Fsup = fitnessSup
        assert self._Fsup < 1.0

    def transferStudent(self, studentID, fromSup, toSup, courses):

        self._graph.transferStudent(studentID, fromSup, toSup, courses)

    def isValid(self, students, courses):

        graph = self._graph
        supEdges = graph.getEdges()
        stuEdges = graph.getStuEdges()

        # If the number of students or courses is not equal to the ones in data, then it's not a valid solution.

        if (len(supEdges) != len(courses)) or (len(stuEdges) != len(students)):
            return False

        for sup in supEdges:

            val = graph.getcourseDegree(sup)

            # if courses degree in solution is greater than their quota limit or 0,then it's not a valid solution.

            if (val > courses[sup].getQuota()) or (val == 0):
                return False

            for stu in supEdges[sup]:

                # If course doesn't exist in their student list or the number of courses for a student is not 1, then it's not a valid solution.

                if (sup not in graph.getcourses(stu)) or (graph.getStudentDegree(stu) != 1):
                    return False

        return True

    def getTransferable(self, courses):

        supEdges = self._graph.getEdges()
        allEdges = set(list(supEdges.keys()))
        canTransferFrom = set()
        canTransferTo = set()

        for sup in supEdges:

            supDegree = len(supEdges[sup])
            quota = courses[sup].getQuota()

            # If course degree is greater than 1 then we can transfer from them
            if (supDegree > 1):
                canTransferFrom.add(sup)

            # If course degree is less than their quota we can transfer to them
            if (supDegree < quota):
                canTransferTo.add(sup)

        return canTransferFrom, canTransferTo

    def getGraph(self):

        return self._graph
