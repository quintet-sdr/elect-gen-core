import argparse
from main import readCoursesInfo, readStudentsInfo, Distribute, writeResults, Course


def main():
    parser = argparse.ArgumentParser(description="Student Course Allocation System")
    parser.add_argument('--read-courses', action='store_true', help='Read courses information from file')
    parser.add_argument('--read-students', action='store_true', help='Read students information from file')
    parser.add_argument('--distribute', action='store_true', help='Distribute students to courses')
    parser.add_argument('--write-results', action='store_true', help='Write the distribution results to file')

    args = parser.parse_args()
    courses = []
    students = []

    if args.read_courses:
        courses = readCoursesInfo()
        print("Courses read successfully.")

    if args.read_students:
        if 'courses' not in locals():
            courses = readCoursesInfo()
        students = readStudentsInfo(courses)
        print("Students read successfully.")

    if args.distribute:
        if 'students' not in locals() or 'courses' not in locals():
            print("Courses and students must be loaded before distribution.")
        else:
            errorCourse = Course(-1, "ERROR", 0)
            Distribute(students, errorCourse)
            print("Distribution completed successfully.")

    if args.write_results:
        if 'students' not in locals():
            print("Students must be loaded before writing results.")
        else:
            writeResults(students)
            print("Results written successfully.")


if __name__ == "__main__":
    main()
