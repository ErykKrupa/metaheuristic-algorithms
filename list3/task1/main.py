import random
import time

POPULATION_SIZE = 20
GENOTYPE_LENGTH = 18
SELECTION_RATE = 0.25
MUTATION_RATE = 0.01


def genetic_algorithm(x, e, max_time):
    end_time = time.time() + max_time
    best_adaptation_ever = xin_she_yang(x, e)
    best_solution_ever = x
    population = [_numbers_to_genotype(x)] * POPULATION_SIZE
    while time.time() < end_time:
        new_population, best_adaptation_for_population, best_solution_for_population \
            = _ranking(_mutate(population + _reproduce(_select(population))), e)
        population = new_population[:POPULATION_SIZE]
        if best_adaptation_for_population < best_adaptation_ever:
            best_adaptation_ever = best_adaptation_for_population
            best_solution_ever = best_solution_for_population
    return best_adaptation_ever, best_solution_ever


def xin_she_yang(x, eps):
    return sum(eps[i] * abs(x[i]) ** (i + 1) for i in range(5))


def _numbers_to_genotype(x):
    return ''.join([''.join(("{0:0" + str(GENOTYPE_LENGTH) + "b}").format(int(i)))
                    for i in [abs(j) * (((2 ** GENOTYPE_LENGTH) - 1) // 5) for j in x]])


def _select(population):
    selected_individuals = [individual for individual in population if random.uniform(0, 1) < SELECTION_RATE]
    if len(selected_individuals) % 2 != 0:
        return selected_individuals[1:0]
    return selected_individuals


def _reproduce(population):
    random.shuffle(population)
    new_generation = []
    for pair in [[population.pop(), population.pop()] for _ in range(len(population) // 2)]:
        i = random.randrange(GENOTYPE_LENGTH * 5 + 1)
        new_generation.append(pair[0][:i] + pair[1][i:])
    return new_generation


def _mutate(population):
    mutated_population = []
    for individual in population:
        individual = list(individual)
        for i in range(len(individual)):
            if random.uniform(0, 1) < 0.01:
                individual[i] = ('1' if individual[i] == '0' else '0')
        mutated_population.append(''.join(individual))
    return mutated_population


def _ranking(population, e):
    ranking = []
    for individual in population:
        x = [_genotype_to_numbers(individual[i:i + GENOTYPE_LENGTH]) for i in
             range(0, len(individual), GENOTYPE_LENGTH)]
        ranking.append((individual, xin_she_yang(x, e), x))
    ranking.sort(key=lambda tuple_: tuple_[1])
    return [row[0] for row in ranking], ranking[0][1], ranking[0][2]


def _genotype_to_numbers(number):
    number = number[::-1]
    summary = sum(int(number[xi]) * (2 ** xi) for xi in range(GENOTYPE_LENGTH))
    return 10 * (summary / (2 ** GENOTYPE_LENGTH - 1)) - 5


if __name__ == '__main__':
    data = [float(i) for i in input().split()]
    best_adaptation, best_solution = genetic_algorithm(data[1:6], data[6:], data[0])
    print(*best_solution, best_adaptation)
