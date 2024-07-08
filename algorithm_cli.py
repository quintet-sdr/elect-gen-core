import argparse
from main import readCoursesInfo, readStudentsInfo, Distribute, writeResults, Course, selectDistribution

def main():
    parser = argparse.ArgumentParser(description="Student Course Allocation System")
    parser.add_argument('--read-courses', action='store_true', help='Read courses information from file')
    parser.add_argument('--read-students', action='store_true', help='Read students information from file')
    parser.add_argument('--distribute', action='store_true', help='Distribute students to courses')
    parser.add_argument('--write-results', action='store_true', help='Write the distribution results to file')
    parser.add_argument('--algorithm', type=str, choices=['gen', 'basic'], default='gen', help='The algorithm to use (gen or basic)')

    args = parser.parse_args()
    courses = []
    students = []
    best_distribution = []
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
            if args.algorithm == 'gen':
                best_distribution = selectDistribution(1)
            elif args.algorithm == 'basic':
                best_distribution = selectDistribution(2)
            else:
                print(f"Unknown algorithm: {args.algorithm}")
                return
            print("Distribution completed successfully.")

    if args.write_results:
        if 'students' not in locals():
            print("Students must be loaded before writing results.")
        else:
            writeResults(best_distribution)
            print("Results written successfully.")


if __name__ == "__main__":
    main()