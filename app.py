import json
from main import startBasicAlgorithm
from excel_util import writeResults
from json_util import readCoursesInfoJson


def run(student_file, course_file, output_file):
    best_distributions, best_distribution_costs, courses_rate_dict = startBasicAlgorithm(student_file,
                                                                                         course_file)
    courses = readCoursesInfoJson(course_file)

    # writeResults(best_distributions, best_distribution_costs, courses, courses_rate_dict)

    all_distributions = {}
    print('Writing output in JSON...')
    for i, distribution in enumerate(best_distributions, 1):
        distribution_data = [{'student': s.ID, 'course': s.finalCourse} for s in distribution]
        all_distributions[f'Distribution {i}, Cost: {best_distribution_costs[i - 1]}'] = distribution_data

    with open(output_file, 'w') as f:
        json.dump(all_distributions, f, indent=4)
    print('Output written in JSON')

# run('students.json', 'courses.json', 'distribution.json')
