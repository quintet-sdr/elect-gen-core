import random
from pystsup.data import Solution
from pystsup.data import BipartiteGraph
from hopcroftkarp import HopcroftKarp
import copy


def simplify(graph, structure, to_check=None, already_set=None):
    to_keep = []
    if not already_set:
        already_set = set()
    stuEdges = graph.getStuEdges()
    supEdges = graph.getEdges()

    if not to_check:
        to_check = set()
        for stu in stuEdges:
            to_check.add(("stu", stu))
        for sup in supEdges:
            to_check.add(("sup", sup))

    while to_check:
        (s_type, s_id) = to_check.pop()
        if (s_type, s_id) in already_set:
            continue
        if s_type == "stu":
            if len(stuEdges[s_id]) == 0:
                already_set.add(("stu", s_id))
            if len(stuEdges[s_id]) == 1:
                sup = stuEdges[s_id][0]
                to_keep.append((sup, s_id))
                graph.removeEdge(sup, s_id)
                structure[sup] = structure[sup] - 1
                if not ("sup", sup) in already_set:
                    to_check.add(("sup", sup))
                already_set.add(("stu", s_id))
        else:
            e = list(supEdges[s_id])
            if structure[s_id] == 0:
                already_set.add(("sup", s_id))
                for stu in e:
                    graph.removeEdge(s_id, stu)
                    to_check = to_check.union(("stu", x) for x in e)
            elif len(e) == structure[s_id] and structure[s_id] > 0:
                for stu in e:
                    to_keep.append((s_id, stu))
                    aux = set(("sup", x) for x in list(stuEdges[stu]) if (not ("sup", x) in already_set) and x != s_id)
                    to_check = to_check.union(aux)
                    graph.removeExcept(s_id, stu)
                    graph.removeEdge(s_id, stu)
                    already_set.add(("stu", stu))

                structure[s_id] = 0
                already_set.add(("sup", s_id))

    return to_keep, already_set


def is_4_cycle(stu, graph):
    courses = graph.getStuEdges()[stu]
    if len(courses) != 2:
        return False
    supEdges = graph.getEdges()
    s1 = set(supEdges[courses[0]])
    s2 = set(supEdges[courses[1]])
    si = s1.intersection(s2)
    if len(si) >= 2:
        return True


def solve_4_cycle(stu, structure, graph, already_set=None):
    # print("Solving 4 cycle for student",stu)
    courses = graph.getStuEdges()[stu]  # We know it is only 2 courses because we only merge 2 solutions!
    supEdges = graph.getEdges()
    sup1 = courses[0]
    sup2 = courses[1]
    # print("Involved courses are",sup1,sup2)

    to_keep = []
    if not already_set:
        already_set = set()
    to_check = set()

    # Who gets the sudent
    selected = courses[random.randint(0, 1)]
    to_keep.append((selected, stu))
    structure[selected] = structure[selected] - 1
    graph.removeEdge(sup1, stu)
    graph.removeEdge(sup2, stu)
    already_set.add(("stu", stu))
    to_check.add(("sup", sup1))
    to_check.add(("sup", sup2))

    return to_keep, to_check, already_set


def random_allocation(stu, structure, graph, already_set=None):
    if not already_set:
        already_set = set()
    courses = list(graph.getStuEdges()[stu])
    supEdges = graph.getEdges()

    selected = random.randint(0, 1)
    sup = courses[selected]
    to_keep = [(sup, stu)]
    structure[sup] = structure[sup] - 1
    graph.removeEdge(courses[0], stu)
    graph.removeEdge(courses[1], stu)
    to_check = set()
    to_check.add(("sup", courses[0]))
    to_check.add(("sup", courses[1]))
    e = list(supEdges[sup])
    for student in e:
        to_check.add(("stu", student))
    already_set.add(("stu", stu))
    return to_keep, to_check, already_set


def hopkroft(graph, structure):
    transformed_graph = {}

    courses = graph.getEdges()
    students = graph.getStuEdges()
    correspondence = {}
    sup_name = 0
    list_courses = [course for course in courses]
    list_students = [student for student in students]
    random.shuffle(list_courses)
    random.shuffle(list_students)
    a_to_b = {}
    for i in range(len(list_students)):
        a_to_b[list_students[i]] = 'stu' + str(i)

    for course in list_courses:
        cardinality = structure[course]
        for i in range(cardinality):
            for stu in courses[course]:
                transformed_graph.setdefault(sup_name, set()).add(a_to_b[stu])
            correspondence[sup_name] = course
            sup_name = sup_name + 1
    m = HopcroftKarp(transformed_graph).maximum_matching()

    result = BipartiteGraph()
    for student in students:
        sup_code = m[a_to_b[student]]
        result.addEdge(correspondence[sup_code], student)
    return result


def sp_crossover(solution1, solution2, courses=None, students=None, k=None):
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()
    already_set = set()

    mergedGraph = graph1.merge(graph2)

    stf1 = solution1.getStructuralFitness(courses)
    stf2 = solution2.getStructuralFitness(courses)

    if random.random() <= (stf1) / (stf1 + stf2):
        structure = graph1.getStructure()
    else:
        structure = graph2.getStructure()

    original_structure = dict(structure)

    result = hopkroft(mergedGraph, original_structure)
    return Solution(result)


def crossover(solution1, solution2, courses=None, students=None, k=None):
    # Merging the two Graphs

    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    mergedGraph = graph1.merge(graph2)

    stuEdges = mergedGraph.getStuEdges()
    supEdges = mergedGraph.getEdges()

    # Randomly getting the structure from the two graphs
    stf1 = solution1.getStructuralFitness(courses)
    stf2 = solution2.getStructuralFitness(courses)

    if random.random() <= (stf1) / (stf1 + stf2):
        structure = graph1.getStructure()
    else:
        structure = graph2.getStructure()

    lockedEdges = set()
    lockedVertices = set()

    allStudents = set(list(stuEdges.keys()))

    result = BipartiteGraph()

    counts = {}  # stores the degree of the courses in the new offspring graph

    for sup in supEdges:
        counts[sup] = 0

    # Simplify first time here
    simplified = True
    prev_count = {}
    while prev_count != counts:
        prev_count = dict(counts)
        for sup in supEdges:
            supDegree = len(supEdges[sup])
            reqDegree = structure[sup]
            for stu in supEdges[sup]:

                if len(stuEdges[stu]) == 1 and not stu in lockedVertices:
                    mergedGraph.removeExcept(sup, stu)
                    result.addEdge(sup, stu)
                    lockedVertices.add(stu)
                    counts[sup] += 1

                    if counts[sup] == reqDegree:
                        toKeep = result.getStudents(sup)
                        toRemove = mergedGraph.getRemainingStu(sup, toKeep)

                        for i in toRemove:
                            mergedGraph.removeEdge(sup, i)

    prev = set()
    toContinue = False

    while len(lockedVertices) != len(stuEdges):

        for sup in supEdges:

            # If the course degree is not equal to degree we want
            if counts[sup] != structure[sup]:

                supDegree = mergedGraph.getcourseDegree(sup)
                reqSupDegree = structure[sup]
                students = mergedGraph.getStudents(sup)

                # Pick a random student that is not locked from the supervior's list of students
                curr = random.choice(students)
                if (curr not in lockedVertices):

                    # If that edge can be locked, then lock it.
                    if mergedGraph.canLock(sup, curr, structure, counts, lockedVertices):

                        # Remove other courses in student's list of courses

                        mergedGraph.removeExcept(sup, curr)

                        # Add it to the new graph and also locked vertices
                        result.addEdge(sup, curr)
                        lockedVertices.add(curr)

                        # Increment the degree of the course
                        counts[sup] += 1

                        # If the degee is the degree we want
                        if counts[sup] == reqSupDegree:

                            toKeep = result.getStudents(sup)  # Get the students we want to keep
                            toRemove = mergedGraph.getRemainingStu(sup, toKeep)  # Get students we dont want to keep

                            # Remove those students (edges)

                            for stu in toRemove:
                                mergedGraph.removeEdge(sup, stu)

        # If we can lock any further, then we break the loop
        if len(prev) != len(lockedVertices):
            prev = set(list(lockedVertices))
        else:
            toContinue = True
            break

    # Allocate remaining students to courses that don't meet the required degree
    if toContinue:
        availableStudents = allStudents.difference(lockedVertices)
        for sup in supEdges:
            reqDegree = structure[sup]
            supDegree = counts[sup]
            supNeeds = reqDegree - supDegree
            if supDegree != reqDegree:
                toAdd = random.sample(availableStudents, supNeeds)
                for stu in toAdd:
                    result.addEdge(sup, stu)
                    lockedVertices.add(stu)
                    counts[sup] += supNeeds
                    availableStudents.remove(stu)

    return Solution(result)


def fixSolution(graph, courses, students):
    supEdges = graph.getEdges()

    # Checking courses that must reduce, and who can get students
    needs = set()
    can_get = {}
    has_reduce = {}
    can_give = {}
    for course in courses:
        if not course in supEdges:
            needs.add(course)
            can_get[course] = courses[course].getQuota()
        else:
            now = len(supEdges[course])
            quota = courses[course].getQuota()
            if now > 1:
                can_give[course] = now - 1
            if now > quota:
                has_reduce[course] = now - quota
            if now < quota:
                can_get[course] = quota - now

    while needs:
        sup1 = random.choice(list(needs))
        if has_reduce:
            where = list(has_reduce.keys())
        else:
            where = list(can_give.keys())
        sup2 = random.choice(where)
        to_transfer = random.choice(supEdges[sup2])
        graph.removeEdge(sup2, to_transfer)
        graph.addEdge(sup1, to_transfer)
        if can_give[sup2] - 1 == 0:
            del can_give[sup2]
        else:
            can_give[sup2] = can_give[sup2] - 1
        if sup2 in has_reduce and has_reduce[sup2] - 1 == 0:
            del has_reduce[sup2]
        elif sup2 in has_reduce:
            has_reduce[sup2] = has_reduce[sup2] - 1
        needs.remove(sup1)
        if can_get[sup1] - 1 == 0:
            del can_get[sup1]
        else:
            can_get[sup1] = can_get[sup1] - 1

    while has_reduce:  # while has to reduce
        sup1 = random.choice(list(has_reduce.keys()))
        sup2 = random.choice(list(can_get.keys()))
        to_transfer = random.choice(supEdges[sup1])
        graph.removeEdge(sup1, to_transfer)
        graph.addEdge(sup2, to_transfer)
        if has_reduce[sup1] - 1 == 0:
            del has_reduce[sup1]
        else:
            has_reduce[sup1] = has_reduce[sup1] - 1
        if can_get[sup2] - 1 == 0:
            del can_get[sup2]
        else:
            can_get[sup2] = can_get[sup2] - 1


def uniform(solution1, solution2, courses, students, k=None):
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    stuEdges1 = graph1.getStuEdges()
    stuEdges2 = graph2.getStuEdges()

    g = BipartiteGraph()
    for stu in students:
        if random.random() < 0.5:
            sup = stuEdges1[stu][0]
        else:
            sup = stuEdges2[stu][0]
        g.addEdge(sup, stu)

    fixSolution(g, courses, students)
    return Solution(g)


def kPoint(solution1, solution2, courses, students, k=5):
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    stuEdges1 = graph1.getStuEdges()
    stuEdges2 = graph2.getStuEdges()
    supEdges1 = graph1.getEdges()

    # Randomly getting the structure from the two graphs

    num = random.randint(1, 2)
    if num == 1:
        structure = graph1.getStructure()
    else:
        structure = graph2.getStructure()

    # Setting up the vectors

    students = list(stuEdges1.keys())
    sol1 = []
    sol2 = []
    for i in range(len(students)):
        sol1.append(stuEdges1[students[i]][0])
        sol2.append(stuEdges2[students[i]][0])

    # Dividing the both solutions into k-points

    sol1Points = []
    sol2Points = []

    points = sorted(random.sample(range(1, len(students)), k))
    curr = 0

    for i in range(k - 1):
        sol1Points.append(sol1[curr:points[i]])
        sol2Points.append(sol2[curr:points[i]])
        curr = points[i]

    sol1Points.append(sol1[curr:])
    sol2Points.append(sol2[curr:])

    # Perform the crossover

    result = []

    if k == 0:
        n = random.randint(1, 2)
        if n == 1:
            result = sol1
        else:
            result = sol2

    else:

        for point in range(k):
            n = random.randint(1, 2)
            if n == 1:
                result.extend(sol1Points[point])
            else:
                result.extend(sol2Points[point])

    graph = BipartiteGraph()
    for i in range(len(students)):
        graph.addEdge(result[i], students[i])

    fixSolution(graph, courses, students)
    return Solution(graph)
