"""JSON utility functions for reading and writing data from and to JSON files and converting Excel files to JSON"""

import pandas as pd
import json
import random
from models import Course, Student


def excel_to_json(excel_file_path, json_file_path):
    """Converts an Excel file to a JSON file
    :param excel_file_path: path to the Excel file
    :param json_file_path: path to the JSON file
    :return: path to the JSON file
    """

    df = pd.read_excel(excel_file_path)
    json_data = df.to_json(orient="records")
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)
    return json_file_path


def format_json_file(file_path):
    """Formats a JSON file
    :param file_path: path to the JSON file
    :return: None
    """

    with open(file_path, 'r') as f:
        data = json.load(f)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def readCoursesInfoJson(path_courses_json):
    with open(path_courses_json, 'r') as f:
        courses_json = json.load(f)
    courses = []
    print(courses_json)
    for course_data in courses_json:
        codename = course_data['codename']
        min_overall = int(course_data['min_overall'])
        low_in_group = int(course_data['low_in_group'])
        high_in_group = int(course_data['high_in_group'])
        max_in_group = int(course_data['max_in_group'])
        max_overall = int(course_data['max_overall'])
        courses.append(Course(codename, min_overall, max_overall, low_in_group, high_in_group, max_in_group))
    return courses


def readStudentsInfoJson(path_students_json):
    with open(path_students_json, 'r') as f:
        students_json = json.load(f)
    students = []
    for student_data in students_json:
        email = student_data['email']
        gpa = float(student_data['gpa'])
        keywords = [student_data['priority_1'], student_data['priority_2'], student_data['priority_3'],
                    student_data['priority_4'], student_data['priority_5']]
        availableCourses = keywords.copy()
        students.append(Student(email, gpa, keywords, availableCourses))
    students.sort(key=lambda student: student.gpa, reverse=True)
    return students
