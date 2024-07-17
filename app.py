import json
from core.main import startBasicAlgorithm
from core.excel_util import writeResults
from core.json_util import readCoursesInfoJson


def run(students_json, courses_json):
    best_distributions, best_distribution_costs, courses_rate_dict = startBasicAlgorithm(students_json,
                                                                                         courses_json)
    # courses = courses_json

    # writeResults(best_distributions, best_distribution_costs, courses, courses_rate_dict)

    all_distributions = {}
    # print('Writing output in JSON...')
    for i, distribution in enumerate(best_distributions, 1):
        distribution_data = [{'student': s.email, 'course': s.finalCourse} for s in distribution]
        all_distributions[f'Distribution {i}, Cost: {best_distribution_costs[i - 1]}'] = distribution_data

    # with open(output_file, 'w') as f:
    #     json.dump(all_distributions, f, indent=4)
    # print('Output written in JSON')
    return all_distributions

# run('students.json', 'courses.json', 'distribution.json')
