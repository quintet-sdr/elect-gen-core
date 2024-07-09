import time
from multiprocessing import Pool
import math
import os
import numpy as np
import random


def calculate_success_rate(num_students):
    if 0 <= num_students <= 16:
        return 0
    elif 17 <= num_students <= 20:
        return math.exp(num_students - 16)
    elif 21 <= num_students <= 28:
        return math.exp(4 - (num_students - 20))
    elif 29 <= num_students <= 34:
        return math.exp(num_students - 28)
    elif 35 <= num_students <= 40:
        return math.exp(6 - (num_students - 34))
    elif 41 <= num_students <= 56:
        return math.exp(num_students - 40)
    elif 57 <= num_students <= 72:
        return math.exp(16 - (num_students - 56))
    elif 73 <= num_students <= 88:
        return math.exp(num_students - 72)
    elif 89 <= num_students <= 104:
        return math.exp(16 - (num_students - 88))
    elif 105 <= num_students <= 120:
        return math.exp(num_students - 104)
    else:
        return 0


success_rate_dict = {i: calculate_success_rate(i) for i in range(0, 10000000)}


def calculate_fitness_helper(args):
    individual, students, courses = args
    return calculate_fitness(individual, students, courses)


def memoize(func):
    cache = dict()

    def memoized_func(*args):
        hashable_args = tuple(tuple(x) if isinstance(x, list) else x for x in args)
        if hashable_args in cache:
            return cache[hashable_args]
        result = func(*args)
        cache[hashable_args] = result
        return result

    return memoized_func


@memoize
def costFunction(students, courses):
    cost = 0
    student_priorities = np.array([student.finalPriority for student in students])
    student_GPAs = np.array([max(student.GPA, 0.1) for student in students])
    cost += np.sum((student_priorities ** 2) / student_GPAs)

    for course in courses:
        numOfStudents = len(course.students)
        cost += success_rate_dict[numOfStudents] ** 4
    return cost


def create_individual(students, courses):
    individual = []
    for student in students:
        course = random.choice(courses)
        individual.append((student.ID, course.ID))
    return individual


def calculate_fitness(individual, students, courses):
    # Create a copy of the students and courses
    students_copy = [student for student in students]
    courses_copy = [course for course in courses]

    # Distribute the students according to the individual
    for student_id, course_id in individual:
        student = next((s for s in students_copy if s.ID == student_id), None)
        course = next((c for c in courses_copy if c.ID == course_id), None)
        if student is not None and course is not None:
            student.finalCourse = course.name
            # Use course name instead of course object
            if course.name in student.availableCourses:
                student.finalPriority = student.availableCourses.index(course.name) + 1
            else:
                student.finalPriority = len(
                    student.availableCourses) + 1  # Assign the lowest priority if the course is not in the availableCourses list
            course.students.append(student)

    # Calculate the cost
    return costFunction(students_copy, courses_copy)  # Pass courses_copy to costFunction


def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]


def tournament_selection(population, fitnesses, tournament_size=5):
    # Select a number of individuals from the population
    tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
    # Return the individual with the best fitness
    return min(tournament, key=lambda x: x[1])[0]


def two_point_crossover(parent1, parent2):
    # Select two crossover points
    crossover_point1 = random.randint(0, len(parent1) - 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)
    # Create the child
    return parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]


def mutate(individual, students, courses, course_quotas):
    index = random.randint(0, len(individual) - 1)
    student_id, course_id = individual[index]
    student = next((s for s in students if s.ID == student_id), None)
    if student is not None:
        course_name_to_object = {course.name: course for course in
                                 courses}
        available_courses = [course_name_to_object[course_name] for course_name in student.availableCourses if
                             course_quotas[course_name_to_object[course_name].ID] > 0]
        if course_id in [course.ID for course in available_courses]:
            course_index = [course.ID for course in available_courses].index(course_id)
            # If there is a lower priority course available, move the student to that course
            if course_index < len(available_courses) - 1:
                old_course_id = course_id
                course_id = available_courses[course_index + 1].ID
                course_quotas[old_course_id] += 1
                course_quotas[course_id] -= 1
        else:
            old_course_id = course_id
            course_id = random.choice(available_courses).ID
            course_quotas[old_course_id] += 1
            course_quotas[course_id] -= 1
    individual[index] = (student_id, course_id)


def hill_climb(individual, students, courses):
    new_individual = individual.copy()

    index1, index2 = random.sample(range(len(individual)), 2)

    student1_id, course1_id = new_individual[index1]
    student2_id, course2_id = new_individual[index2]

    student1 = next((s for s in students if s.ID == student1_id), None)
    student2 = next((s for s in students if s.ID == student2_id), None)

    course_name_to_object = {course.name: course for course in courses}  # Create a dictionary to map course names to Course objects
    course1 = next((c for c in student1.availableCourses if course_name_to_object[c].ID == course1_id), None)
    course2 = next((c for c in student2.availableCourses if course_name_to_object[c].ID == course2_id), None)

    # Check if both courses are in the priority list of both students
    if course1 in student2.availableCourses and course2 in student1.availableCourses:
        # Swap their courses
        new_individual[index1], new_individual[index2] = new_individual[index2], new_individual[index1]

    # If the new individual has better fitness, return it
    if calculate_fitness(new_individual, students, courses) < calculate_fitness(individual, students, courses):
        return new_individual

    # Otherwise, return the original individual
    return individual


def genetic_algorithm(students, courses, num_generations=100, population_size=100, mutation_rate=0.03,
                      elitism_rate=0.1):
    # Start timing the initial population generation
    start_time_population = time.time()

    # Create the initial population
    population = [create_individual(students, courses) for _ in range(population_size)]

    # End timing the initial population generation
    end_time_population = time.time()
    print(f"Time spent on generating initial population: {end_time_population - start_time_population} seconds")

    # Save the initial quotas
    initial_course_quotas = [course.quota for course in courses]

    # Start timing the GA work
    start_time_ga = time.time()

    for _ in range(num_generations):
        # Reset the quotas to their initial values
        for i, course in enumerate(courses):
            course.quota = initial_course_quotas[i]

        # Create a copy of the quotas for this generation
        course_quotas = [course.quota for course in courses]

        # Calculate the fitness of each individual in the population
        with Pool() as pool:
            fitnesses = pool.map(calculate_fitness_helper,
                                 [(individual, students, courses) for individual in population])

        # Create the next generation
        next_population = []

        # Implement elitism
        num_elites = int(elitism_rate * population_size)
        elites = sorted(zip(population, fitnesses), key=lambda x: x[1])[:num_elites]
        next_population.extend(individual for individual, fitness in elites)

        while len(next_population) < population_size:
            # Select two parents using tournament selection
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            # Create a child using two-point crossover and mutate it
            child = two_point_crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(child, students, courses, course_quotas)

            # Apply hill climbing to the child
            child = hill_climb(child, students, courses)

            # Add the child to the next generation
            next_population.append(child)

        # Replace the current population with the next generation
        population = next_population

        print(f"Generation: {_ + 1}, Best Fitness: {min(fitnesses)}")

    # End timing the GA work
    end_time_ga = time.time()
    print(f"Time spent on GA work: {end_time_ga - start_time_ga} seconds")

    # Return the best individual from the final population
    return min(population, key=lambda individual: calculate_fitness(individual, students, courses))
