import argparse
from main import startBasicAlgorithm
from json_util import excel_to_json, format_json_file, readCoursesInfoJson
from excel_util import writeResults
import json


def main():
    parser = argparse.ArgumentParser(prog='elect-gen-core', description="Student Course Allocation System")
    parser.add_argument('--convert', action='store_true', help='Convert Excel files to JSON')
    parser.add_argument('--courses', type=str, help='Path to courses Excel file')
    parser.add_argument('--students1', type=str, help='Path to first students Excel file')
    parser.add_argument('--students2', type=str, help='Path to second students Excel file')
    parser.add_argument('--output', type=str, help='Path to output JSON file')

    args = parser.parse_args()

    if args.convert:
        print('Converting to JSON...')
        format_json_file(excel_to_json(args.courses, 'courses.json'))
        print('Courses converted to JSON')
        print('Converting to JSON...')
        format_json_file(excel_to_json(args.students1, 'students1.json'))
        print('Students1 converted to JSON')
        print('Converting to JSON...')
        format_json_file(excel_to_json(args.students2, 'students2.json'))
        print('Students2 converted to JSON \n Merging students...')
        with open('students1.json', 'r') as f1, open('students2.json', 'r') as f2, open('students.json', 'w') as f_out:
            students1 = json.load(f1)
            students2 = json.load(f2)
            students = students1 + students2
            json.dump(students, f_out, indent=4)
            print('Students merged')
    else:
        courses = readCoursesInfoJson('courses.json')
        best_distributions, best_distribution_costs = startBasicAlgorithm(args.students1, args.courses)

        writeResults(best_distributions, best_distribution_costs, courses)

        all_distributions = {}
        print('Writing output in JSON...')
        for i, distribution in enumerate(best_distributions, 1):
            distribution_data = [{'student': s.ID, 'course': s.finalCourse} for s in distribution]
            all_distributions[f'Distribution {i}, Cost: {best_distribution_costs[i - 1]}'] = distribution_data

        with open(args.output, 'w') as f:
            json.dump(all_distributions, f, indent=4)
        print('Output written in JSON')


if __name__ == "__main__":
    main()
