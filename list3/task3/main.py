import sys
from random import randrange
from time import time
from agent import *
import numpy as np

POPULATION = 4


def genetic_algorithm(max_time, board, paths, p):
    population = paths
    best_solution_ever = None
    best_adaptation_ever = np.inf
    end_time = time() + max_time
    while time() < end_time:
        adaptations = []
        for individual in population:
            individual, adaptation = _get_adaptation(individual, board)
            adaptations.append(adaptation)
            if adaptation < best_adaptation_ever:
                best_solution_ever = individual
                best_adaptation_ever = adaptation
        new_population = []
        for _ in range(p // 2):
            mother = population[_select(adaptations)]
            father = population[_select(adaptations)]
            daughter, son = _reproduce(mother, father)
            new_population += [_mutate(daughter), _mutate(son)]
        population = new_population
    return best_solution_ever, best_adaptation_ever


def _get_adaptation(path, board):
    agent = Agent(board)
    adaptation = 0
    minimalized_path = []
    for step in path:
        if adaptation > board.size:
            return path, np.inf
        if agent.look_down(step) == Agent.EXIT:
            minimalized_path.append(agent.move(step))
            adaptation += 1
            return minimalized_path, adaptation
        if agent.look_down(step) != Agent.WALL:
            minimalized_path.append(agent.move(step))
            adaptation += 1
    return path, np.inf


def _select(adaptations):
    adaptation_amount = len(adaptations)
    best_adaptation = randrange(adaptation_amount)
    for i in range(1, POPULATION):
        adaptation = randrange(adaptation_amount)
        if adaptations[adaptation] < adaptations[best_adaptation]:
            best_adaptation = adaptation
    return best_adaptation


def _reproduce(mother, father):
    daughter = mother.copy()
    son = father.copy()
    min_path_size = min(len(daughter), len(son))
    pivot_left = randrange(min_path_size)
    pivot_right = randrange(min_path_size)
    if pivot_left > pivot_right:
        pivot_left, pivot_right = pivot_right, pivot_left
    if pivot_left != pivot_right:
        for i in range(pivot_left, pivot_right):
            daughter[i], son[i] = son[i], daughter[i]
    return daughter, son


def _mutate(individual):
    i = randrange(len(individual))
    j = randrange(len(individual))
    individual[i], individual[j] = individual[j], individual[i]
    return individual


if __name__ == '__main__':
    max_time, n, m, s, p = input().split()
    matrix = np.array([[int(char) for char in input()] for _ in range(int(n))])
    paths = [[step for step in input()] for _ in range(int(s))]
    agent = Agent(matrix)
    best_solution, best_adaptation = genetic_algorithm(float(max_time), matrix, paths, int(p))
    print(best_adaptation)
    print(''.join(best_solution), file=sys.stderr)
