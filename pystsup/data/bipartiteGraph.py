import random
import copy


class BipartiteGraph:

    def __init__(self, edges=None, edges_Stu=None):
        if edges_Stu:
            self._edgesStu = edges_Stu
        else:
            self._edgesStu = {}

        if edges:
            self._edges = edges
        else:
            self._edges = {}

    def convertToTuple(self, edges):

        d = {}
        for key, val in edges.items():
            d[key] = tuple(val)

        return d

    def __key(self):
        d = self.convertToTuple(self._edgesStu)

        return frozenset(d.items())

    def __hash__(self):

        return hash(self.__key())

    def __eq__(self, graph2):

        return self._edgesStu == graph2.getStuEdges()

    def addEdge(self, course, student):

        # Adding only if it is a new edge

        if (self.isEdge(course, student) == False):

            if self.courseExists(course):
                self._edges[course].append(student)
            else:
                self._edges[course] = [student]

            if self.studentExists(student):
                self._edgesStu[student].append(course)
            else:
                self._edgesStu[student] = [course]

    def removeEdge(self, course, student):

        self._edges[course].remove(student)
        self._edgesStu[student].remove(course)

    def isEdge(self, course, student):

        try:
            if (student in self._edges[course]) and (course in self._edgesStu[student]):
                return True
            else:
                return False

        except KeyError:
            return False

    def courseExists(self, course):

        if course in self._edges:
            return True
        else:
            return False

    def studentExists(self, student):

        if student in self._edgesStu:
            return True
        else:
            return False

    def getStudents(self, course):

        return self._edges[course]

    def getCourses(self, student):

        return self._edgesStu[student]

    def getCourseDegree(self, course):

        return len(self._edges[course])

    def getStudentDegree(self, student):

        return len(self._edgesStu[student])

    def createRandomGraph(students, courses):
        edges_Sup = {}
        edges_Stu = {}

        students_left = dict(students)
        courses_left = dict(courses)

        # Allocating a single student to a course
        for sup in courses:
            supId = courses[sup].getcourseID()
            quota = courses[sup].getQuota()

            # Find a student who prefers this course
            for stuId, student in students_left.items():
                if supId in student.getKeywords():
                    # Adding the edge to graph
                    edges_Sup.setdefault(supId, []).append(stuId)
                    edges_Stu[stuId] = [supId]

                    # Removing the allocated student
                    del students_left[stuId]

                    # Checking whether to remove course or not
                    if len(edges_Sup[supId]) >= quota:
                        del courses_left[supId]

                    # Break the loop as we have found a student for this course
                    break

        # Allocating remaining students
        while len(students_left) > 0:
            stuId = random.choice(list(students_left.keys()))
            preferred_courses = students_left[stuId].getKeywords()

            # Pick a course from the student's preferred courses that still has quota
            supId = None
            for course in preferred_courses:
                if course in courses_left and len(edges_Sup[course]) < courses_left[course].getQuota():
                    supId = course
                    break

            # If no preferred course has quota, pick a random course
            if supId is None:
                supId = random.choice(list(courses_left.keys()))

            quota = courses_left[supId].getQuota()

            # Adding the edge to graph
            # print(edges_Sup, '\n---\n')
            # print(supId, '\n---\n')
            # print(courses_left, '\n---\n')
            edges_Sup.setdefault(supId, []).append(stuId)
            edges_Stu[stuId] = [supId]

            del students_left[stuId]

            if len(edges_Sup[supId]) >= quota:
                del courses_left[supId]

        return BipartiteGraph(edges_Sup, edges_Stu)




    # def createRandomGraph(students, courses):
    #     edges_Sup = {}
    #     edges_Stu = {}
    #
    #     students_left = dict(students)
    #     courses_left = dict(courses)
    #
    #     # Allocating a single student to a course
    #     for sup in courses:
    #         supId = courses[sup].getcourseID()
    #         quota = courses[sup].getQuota()
    #         # print("Course ID: ", supId, "Quota: ", quota)
    #
    #         # Find a student who prefers this course
    #         for stuId, student in students_left.items():
    #             if supId in student.getKeywords():
    #                 # print("Student ID: ", stuId, "Keywords: ", student.getKeywords())
    #                 # Adding the edge to graph
    #                 edges_Sup.setdefault(supId, []).append(stuId)
    #                 edges_Stu[stuId] = [supId]
    #
    #                 # Removing the allocated student
    #                 del students_left[stuId]
    #
    #                 # Checking whether to remove course or not
    #                 if len(edges_Sup[supId]) >= quota:
    #                     del courses_left[sup]
    #
    #                 # Break the loop as we have found a student for this course
    #                 break
    #         # print("--break--")
    #
    #     # Allocating remaining students
    #
    #     while len(students_left) > 0:
    #         supId = random.choice(list(courses_left.keys()))
    #         quota = courses_left[supId].getQuota()
    #         stuId = random.choice(list(students_left.keys()))
    #
    #         # Adding the edge to graph
    #
    #         edges_Sup[supId].append(stuId)
    #         edges_Stu[stuId] = [supId]
    #
    #         del students_left[stuId]
    #
    #         if len(edges_Sup[supId]) >= quota:
    #             del courses_left[supId]
    #
    #
    #
    #     while len(students_left) > 0:
    #         print("Students left: ", len(students_left))
    #         stuId = random.choice(list(students_left.keys()))
    #         preferred_courses = students_left[stuId].getKeywords()
    #
    #         for supId in preferred_courses:
    #             supId = 'course' + str(supId)
    #             result = [item[0] for item in list(preferred_courses.values())]
    #             if courses_left[supId].getCourseName().lower() in result:
    #
    #                 quota = courses_left[supId].getQuota()
    #                 print("Course ID: ", supId, "Quota: ", quota, "Student ID: ", stuId, "Keywords: ",
    #                       result)
    #                 print("------")
    #                 print(edges_Sup)
    #                 if len(edges_Sup[supId]) < quota:
    #                     # Adding the edge to graph
    #                     edges_Sup[supId].append(stuId)
    #                     edges_Stu[stuId] = [supId]
    #
    #                     del students_left[stuId]
    #
    #                     if len(edges_Sup[supId]) >= quota:
    #                         del courses_left[supId]
    #                     break
    #         # else:
    #         #     # If all preferred courses are full, choose a random course
    #         #     supId = random.choice(list(courses_left.keys()))
    #         #     edges_Sup[supId].append(stuId)
    #         #     edges_Stu[stuId] = [supId]
    #         #
    #         #     del students_left[stuId]
    #         #
    #         #     if len(edges_Sup[supId]) >= quota:
    #         #         del courses_left[supId]
    #
    #
    #
    #
    #     # while len(students_left) > 0:
    #     #
    #     #     stuId = random.choice(list(students_left.keys()))
    #     #     print(students_left, '\n---\n')
    #     #     print(stuId, '\n---\n')
    #     #     print(students_left[stuId], '\n---\n')
    #     #     print(list(students_left[stuId].getKeywords()), '\n---\n')
    #     #     preferred_courses = [item[0] for item in list(students_left[stuId].getKeywords())]
    #     #
    #     #     # Pick a course from the student's preferred courses that still has quota
    #     #     supId = None
    #     #     for course in preferred_courses:
    #     #         if course in courses_left and len(edges_Sup[course]) < courses_left[course].getQuota():
    #     #             supId = course
    #     #             break
    #     #
    #     #     # If no preferred course has quota, pick a random course
    #     #     if supId is None:
    #     #         supId = random.choice(list(courses_left.keys()))
    #     #
    #     #     quota = courses_left[supId].getQuota()
    #     #
    #     #     # Adding the edge to graph
    #     #     edges_Sup[supId].append(stuId)
    #     #     edges_Stu[stuId] = [supId]
    #     #
    #     #     del students_left[stuId]
    #     #
    #     #     if len(edges_Sup[supId]) >= quota:
    #     #         del courses_left[supId]
    #
    #     return BipartiteGraph(edges_Sup, edges_Stu)

    def transferStudent(self, studentID, fromSup, toSup, courses):

        # Transfers only when the following conditions are met i.e when a transfer is possible

        if (self.getCourseDegree(fromSup) >= 2) and (
                self.getCourseDegree(toSup) + 1 <= courses[toSup].getQuota()):

            if (self.studentExists(studentID)) and (self.isEdge(fromSup, studentID)):
                self.addEdge(toSup, studentID)
                self.removeEdge(fromSup, studentID)

    def transferStudent1(self, studentID, fromSup, toSup, courses):

        self.addEdge(toSup, studentID)
        self.removeEdge(fromSup, studentID)

    def swapStudents(self, student1, course1, student2, course2):

        self.removeEdge(course1, student1)
        self.removeEdge(course2, student2)
        self.addEdge(course1, student2)
        self.addEdge(course2, student1)

    def getStructure(self):

        structure = {}

        for sup in self._edges:
            structure[sup] = len(self._edges[sup])

        return structure

    def merge(self, graph2):

        # Making a deepcopy so that the original graph edges are not disturbed.

        graph2_Edges = copy.deepcopy(graph2.getEdges())  # Get graph2 edges
        edges_Stu = copy.deepcopy(self._edgesStu)
        edges_Sup = copy.deepcopy(self._edges)

        for sup in edges_Sup:
            a = set(edges_Sup[sup])  # Get Students in graph1
            b = set(graph2_Edges[sup])  # Get students in graph2

            # Get thier difference, and the ones that are not present in graph1 to graph1

            for stu in (b.difference(a)):
                edges_Sup[sup].append(stu)
                edges_Stu[stu].append(sup)

        return BipartiteGraph(edges_Sup, edges_Stu)

    def getRemainingSup(self, course, student):

        for sup in self._edgesStu[student]:
            if sup != course:
                return sup

    def removeExcept(self, course, student):

        for sup in self._edgesStu[student]:
            if sup != course:
                self.removeEdge(sup, student)

    def removeExceptSup(self, course, student, reqStructure):

        for stu in self._edges[course]:
            if stu != student and (self.getCourseDegree(course) - 1 >= reqStructure):
                self.removeEdge(course, stu)

    def getRemainingStu(self, course, studentList):

        stuList = set(self._edges[course])
        toRemove = stuList - set(studentList)

        return toRemove

    def canLock(self, sup, stu, structure, counts, lockedVertices):

        # If the student has only 1 course, it has to be locked.

        if self.getStudentDegree(stu) == 1:
            return True

        else:

            remainingSup = self.getRemainingSup(sup, stu)  # Get the other course
            stuList = set(self.getStudents(remainingSup))  # Get the list of students of the other course

            # availableStu = self.getAvailableEdges(remainingSup,lockedVertices)

            availableStu = stuList - lockedVertices  # Get list of students that are not locked from the other course

            if (structure[remainingSup] - counts[remainingSup]) < len(availableStu):
                return True
            else:
                return False

    def getAvailableEdges(self, sup, lockedVertices):

        available = set()
        students = self.getStudents(sup)

        for stu in students:
            if stu not in lockedVertices:
                available.add(stu)

        return available

    def getNumberofEdges(self):
        return sum(list(self.getStructure().values()))

    def getEdges(self):
        return self._edges

    def getStuEdges(self):
        return self._edgesStu

    def copy(self):

        edges_Stu = copy.deepcopy(self._edgesStu)
        edges_Sup = copy.deepcopy(self._edges)

        return BipartiteGraph(edges_Sup, edges_Stu)

    def getAllEdges(self):

        allEdges = set()
        for sup in self._edges:
            for stu in supEdges[sup]:
                allEdges.add((stu, sup))

        return allEdges
