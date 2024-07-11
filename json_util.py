import pandas as pd
import json
import random
from models import Course, Student


def excel_to_json(excel_file_path, json_file_path):
    df = pd.read_excel(excel_file_path)
    json_data = df.to_json(orient="records")
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)
    return json_file_path


def format_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def readCoursesInfoJson(file_path):
    with open(file_path, 'r') as f:
        courses_data = json.load(f)
    courses = [Course(data.get('ID', -1), data.get('Course', "ERROR"),
                      data.get('Quota', 0)) for data in courses_data]
    return courses


def readStudentsInfoJson(courses, students, file_path):
    with open(file_path, 'r') as f:
        students_data = json.load(f)
    for student_data in students_data:
        ID = student_data.get('Student ID', -1)
        name = student_data.get('Student Name', "ERROR")
        GPA = student_data.get('GPA', 0)
        keywords = []
        availableCourses = []
        for i in range(1, 6):
            keyword = student_data.get(f'Keyword {i}', "ERROR")
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
        GPA = float(GPA)
        if len(availableCourses) < 5:
            other_courses = [course.name for course in courses if course.name not in availableCourses]
            random_courses = random.sample(other_courses, 5 - len(availableCourses))
            availableCourses += random_courses

        students.append(Student(ID, name, GPA, keywords, availableCourses))
    students.sort(key=lambda student: student.GPA, reverse=True)
