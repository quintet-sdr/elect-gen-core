import argparse
from main import readCoursesInfo, readStudentsInfo, Distribute, writeResults, Course, selectDistribution, \
    readCoursesInfoJson
from excel_to_json import excel_to_json, format_json_file
import json


def main():
    parser = argparse.ArgumentParser(prog='elect-gen-core', description="Student Course Allocation System")
    parser.add_argument('--convert_to_json', action='store_true', help='Convert Excel files to JSON')
    parser.add_argument('--courses', type=str, help='Path to courses Excel file')
    parser.add_argument('--students1', type=str, help='Path to first students Excel file')
    parser.add_argument('--students2', type=str, help='Path to second students Excel file')
    parser.add_argument('--output', type=str, help='Path to output JSON file')

    args = parser.parse_args()

    if args.convert_to_json:
        format_json_file(excel_to_json(args.courses, 'courses.json'))
        format_json_file(excel_to_json(args.students1, 'students1.json'))
        format_json_file(excel_to_json(args.students2, 'students2.json'))
        with open('students1.json', 'r') as f1, open('students2.json', 'r') as f2, open(args.output, 'w') as f_out:
            students1 = json.load(f1)
            students2 = json.load(f2)
            students = students1 + students2
            json.dump(students, f_out, indent=4)
    else:
        courses = readCoursesInfoJson('courses.json')
        best_distributions, best_distribution_costs = selectDistribution(2)
        print(', '.join(course.name for course in courses))
        writeResults(best_distributions, best_distribution_costs, courses)

        all_distributions = {}
        for i, distribution in enumerate(best_distributions, 1):
            distribution_data = [{'student': s.ID, 'course': s.finalCourse} for s in distribution]
            all_distributions[f'Distribution {i}, Cost: {best_distribution_costs[i - 1]}'] = distribution_data

        with open(args.output, 'w') as f:
            json.dump(all_distributions, f, indent=4)


if __name__ == "__main__":
    main()
