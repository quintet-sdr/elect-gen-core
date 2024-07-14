"""Excel utility functions for reading and writing data from and to Excel files"""

import os
import random
from models import Course, Student
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


def readCoursesInfo():
    """Reads course information from the Courses.xlsx file and returns a list of Course objects
    :return: list of Course objects
    """

    courseFile = 'Courses.xlsx'

    # Read the Excel file into a DataFrame
    df = pd.read_excel(courseFile)

    courses = []
    for _, row in df.iterrows():
        ID = row[0]
        name = row[1]
        quota = row[2]
        courses.append(Course(ID, name, quota))
    return courses


def readStudentsInfo(courses, students, name):
    """Reads student information from the given Excel file and appends the students to the given list
    :param courses: list of Course objects
    :param students: list of Student objects
    :param name: name of the Excel file
    :return: None
    """

    # Read the Excel file into a DataFrame
    df = pd.read_excel(name)

    for _, row in df.iterrows():
        ID = row[0]
        name = row[1]
        GPA = float(row[2])
        keywords = []
        availableCourses = []
        for j in range(3, 8):
            keyword = row[j]
            flag = False
            for course in courses:
                if course.name.lower() == keyword.lower():
                    flag = True
                    keywords.append(course)
                    if course.ID != -1:
                        availableCourses.append(course.name)
                    break
            if not flag:
                course = Course(-1, keyword, 0)
                courses.append(course)
                keywords.append(course)
        if len(availableCourses) < 5:
            other_courses = [course.name for course in courses if course.name not in availableCourses]
            random_courses = random.sample(other_courses, 5 - len(availableCourses))
            availableCourses += random_courses

        students.append(Student(ID, name, GPA, keywords, availableCourses))
    students.sort(key=lambda student: student.GPA, reverse=True)


def writeResults(students_distributions, costs, courses, courses_rate_dict):
    """Writes the results of the algorithm in an Excel file
    :param students_distributions: list of lists of Student objects
    :param costs: list of costs
    :param courses: list of Course objects
    :param courses_rate_dict: dictionary of course rates
    :return: None
    """

    print("Writing results in table...")
    if "Results.xlsx" in os.listdir():
        os.remove("Results.xlsx")
    writer = pd.ExcelWriter('Results.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Plots and Results')
    writer.sheets['Plots and Results'] = worksheet

    row = 0
    col = 0
    plot_height = 24  # Adjust based on your plot size

    for course in courses:
        # Retrieve x and y values for the current course from courses_rate_dict
        x_values = list(courses_rate_dict[course.name].keys())
        y_values = list(courses_rate_dict[course.name].values())
        y_values = [-y for y in y_values]

        # Generate and save plot to a buffer
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values)
        ax.set_title(f'Success Rate for {course.name}')
        ax.set_xlabel('Number of Students')
        ax.set_ylabel('Success Rate')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Insert plot into the worksheet
        worksheet.insert_image(row, col, f'{course.name}.png', {'image_data': buffer})
        row += plot_height  # Move to the next plot position

    # After plots, write the algorithm results
    # Adjust `row` as needed to place the data below the last plot
    numeration = 1
    costs_dict = {cost: students for students, cost in zip(students_distributions, costs)}
    for cost, students in costs_dict.items():
        totalResults = [0] * 7
        totalCourseResults = [0] * len(courses)
        totalCourseQuotas = [course.quota for course in courses]
        totalCourseNames = [course.name for course in courses]
        for student in students:
            if 1 <= student.finalPriority <= 7:
                totalResults[student.finalPriority - 1] += 1
            matching_courses = [course for course in courses if course.name == student.finalCourse]
            if matching_courses:
                totalCourseResults[courses.index(matching_courses[0])] += 1
        max_length = max(len(totalResults), len(totalCourseResults), len(totalCourseQuotas), len(totalCourseNames))
        totalResults.extend([0] * (max_length - len(totalResults)))
        totalCourseResults.extend([0] * (max_length - len(totalCourseResults)))
        totalCourseQuotas.extend([0] * (max_length - len(totalCourseQuotas)))
        totalCourseNames.extend([""] * (max_length - len(totalCourseNames)))
        statistics_data = {'Total Results': totalResults, 'Total Course Results': totalCourseResults,
                           'Total Course Quotas': totalCourseQuotas, 'Total Course Names': totalCourseNames}
        df_statistics = pd.DataFrame(statistics_data)
        df_statistics.to_excel(writer, sheet_name=f'Result {numeration}', index=False)
        data = {'Student ID': [student.ID for student in students],
                'Student Name': [student.name for student in students],
                'Final priority': [student.finalPriority for student in students],
                'Course Name': [student.finalCourse for student in students],
                'Actual Course Name': [
                    student.keywords[student.finalPriority - 1].name if student.finalPriority <= 5 else "" for student
                    in students]}
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name=f'Result {numeration}', startrow=len(df_statistics) + 2, index=False)
        numeration += 1
    writer._save()

    print("Results written in table")
