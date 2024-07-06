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

        for course in [course[0] for course in list(preferred_courses.values())]:
            print('course:', course, '\n\npreferred_courses:',
                  [course[0] for course in list(preferred_courses.values())], '\n\ncourses_left:',
                  [course.getCourseName().lower() for course in list(courses_left.values())])
            print('---\n', edges_Sup, '\n---\n', course, '\n---\n', courses_left, '\n---\n')
            if course in [course_t.getCourseName().lower() for course_t in list(courses_left.values())]:
                if len(edges_Sup[course]) < courses_left[course].getQuota():
                    supId = course
                    break

        # If no preferred course has quota, pick a random course
        # if supId is None:
        #     supId = random.choice(list(courses_left.keys()))

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