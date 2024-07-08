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
    course_quotas = {course.ID: course.quota for course in courses}  # Create a dictionary to track course quotas

    for student in students:
        available_courses = [course for course in student.availableCourses if course_quotas[course.ID] > 0]
        if available_courses:  # Check if there are available courses
            course = random.choice(available_courses)
            individual.append((student.ID, course.ID))
            course_quotas[course.ID] -= 1  # Decrease the quota of the selected course

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
    cost = 0
    for student in students_copy:
        if student.finalPriority == 7 or student.GPA == 0:
            continue
        cost += (student.finalPriority ** 2) / student.GPA

    # Add a penalty for each course where the quota is exceeded
    for course in courses_copy:
        if len(course.students) > course.quota:
            cost += (len(course.students) - course.quota) * 10000  # penalty_factor is a constant to be defined

    return cost


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
        available_courses = [course.ID for course in student.availableCourses if course_quotas[course.ID] > 0]
        if course_id in available_courses:
            course_index = available_courses.index(course_id)
            # If there is a lower priority course available, move the student to that course
            if course_index < len(available_courses) - 1:
                old_course_id = course_id
                course_id = available_courses[course_index + 1]
                course_quotas[old_course_id] += 1  # Increase the quota of the old course
                course_quotas[course_id] -= 1  # Decrease the quota of the selected course
        else:
            print("Invalid course for student")
            print("All courses: ", [course.ID for course in courses])
            print("Quotas: ", [len(course.students) for course in courses])
            print("Correct quotas: ", course_quotas)
            print("Available courses: ", [course.ID for course in student.availableCourses])
            # If the current course is not in the student's available courses, choose a random course
            old_course_id = course_id
            course_id = random.choice(available_courses)
            course_quotas[old_course_id] += 1  # Increase the quota of the old course
            course_quotas[course_id] -= 1  # Decrease the quota of the selected course
    individual[index] = (student_id, course_id)


def genetic_algorithm(students, courses, num_generations=500, population_size=500, mutation_rate=0.01,
                      elitism_rate=0.1):
    # Create the initial population
    population = [create_individual(students, courses) for _ in range(population_size)]

    for _ in range(num_generations):
        # Create a copy of the quotas for this generation
        course_quotas = [course.quota for course in courses]

        # Calculate the fitness of each individual in the population
        fitnesses = [calculate_fitness(individual, students, courses) for individual in population]

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

            # Add the child to the next generation
            next_population.append(child)

        # Replace the current population with the next generation
        population = next_population

        print(f"Generation: {_ + 1}, Best Fitness: {min(fitnesses)}")

    # Return the best individual from the final population
    return min(population, key=lambda individual: calculate_fitness(individual, students, courses))
