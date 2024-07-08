import random


def costFunction(students):
    cost = 0
    for student in students:
        if student.finalPriority == 7 or student.GPA == 0:
            continue
        cost += (student.finalPriority ** 2) / student.GPA
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
        course = next((c for c in student.availableCourses if c.ID == course_id), None)
        if student is not None and course is not None:
            student.finalCourse = course.name
            student.finalPriority = student.availableCourses.index(course) + 1
            course.students.append(student)

    # Calculate the cost
    return costFunction(students_copy)


def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]


def mutate(individual, courses):
    index = random.randint(0, len(individual) - 1)
    student_id, course_id = individual[index]
    course_id = random.choice([course.ID for course in courses if course.ID != course_id])
    individual[index] = (student_id, course_id)


def genetic_algorithm(students, courses, num_generations=100, population_size=100, mutation_rate=0.01):
    # Create the initial population
    population = [create_individual(students, courses) for _ in range(population_size)]

    for _ in range(num_generations):
        # Calculate the fitness of each individual in the population
        fitnesses = [calculate_fitness(individual, students, courses) for individual in population]

        # Select two parents
        parent1 = min(random.sample(list(zip(population, fitnesses)), 5), key=lambda x: x[1])[0]
        parent2 = min(random.sample(list(zip(population, fitnesses)), 5), key=lambda x: x[1])[0]

        # Create a child and mutate it
        child = crossover(parent1, parent2)
        if random.random() < mutation_rate:
            mutate(child, courses)

        # Replace the worst individual in the population with the child
        worst_individual = max(population, key=lambda individual: calculate_fitness(individual, students, courses))
        population.remove(worst_individual)
        population.append(child)
        print(f"Generation: {_ + 1}, Best Fitness: {min(fitnesses)}")

    # Return the best individual from the final population
    return min(population, key=lambda individual: calculate_fitness(individual, students, courses))
