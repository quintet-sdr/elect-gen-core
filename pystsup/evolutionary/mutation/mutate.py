import random
from pystsup.data import Solution
import copy


def mutate(solution, courses, probability, swapProbability, transferProbability):
    # Make a copy of the solution graph
    graph = solution.getGraph().copy()

    # Get the list of courses to and from whom we can transfer
    canTransferFrom, canTransferTo = solution.getTransferable(courses)

    supEdges = copy.deepcopy(graph.getEdges())
    stuEdges = copy.deepcopy(graph.getStuEdges())

    allStudents = set(list(stuEdges.keys()))
    allcourses = set(list(supEdges.keys()))

    probSum = swapProbability + transferProbability
    swapProbability = swapProbability / probSum
    transferProbability = transferProbability / probSum

    count = 0

    for sup in supEdges:

        for stu in supEdges[sup]:

            if graph.isEdge(sup, stu):

                n = random.random()

                if n <= probability:

                    count += 1

                    m = random.random()

                    if m <= transferProbability and (graph.getcourseDegree(sup) > 1) and not (
                            len(canTransferTo) == 1 and (sup in canTransferTo)) and len(canTransferTo) > 0:
                        # Perform Transfer Operation

                        if sup in canTransferTo:
                            canTransferTo.remove(sup)

                        toSup = random.choice(list(canTransferTo))

                        graph.transferStudent1(stu, sup, toSup, courses)

                        canTransferTo.add(sup)

                        if not (graph.getcourseDegree(toSup) < courses[toSup].getQuota()):
                            canTransferTo.remove(toSup)


                    else:

                        # Peform Swap Operation

                        allcourses.remove(sup)

                        sup2 = random.choice(list(allcourses))

                        stu2 = random.choice(graph.getStudents(sup2))

                        graph.swapStudents(stu, sup, stu2, sup2)

                        allcourses.add(sup)

    return Solution(graph)
