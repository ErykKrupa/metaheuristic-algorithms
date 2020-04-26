import math
import random
from time import time

import numpy as np

initial_temperature = 200
temperature_change_factor = 0.01


def salomon_function(x: np.ndarray):
    sqrt_of_powers = math.sqrt(sum(x ** 2))
    return 1.0 - math.cos(2 * math.pi * sqrt_of_powers) + 0.1 * sqrt_of_powers


def get_random_neighbour(x: np.ndarray):
    return x + x * (np.random.random(4) * 2 - 1)


def simulated_annealing(starting_solution, max_execution_time):
    def probability():
        return 1.0 / (1.0 + np.power(np.e, -1 * delta) / temperature)

    end_time = time() + max_execution_time
    temperature = initial_temperature
    current_solution = starting_solution
    temperature_change = 1 - temperature_change_factor
    while time() < end_time and temperature > 0.001:
        new_solution = get_random_neighbour(current_solution)
        delta = salomon_function(new_solution) - salomon_function(current_solution)
        if delta <= 0 or probability() > random.random():
            current_solution = new_solution
        temperature *= temperature_change
    return current_solution, salomon_function(current_solution)


if __name__ == '__main__':
    time_, *_initial_solution = input().split()
    solution, value = simulated_annealing(np.array([int(x) for x in _initial_solution]), int(time_))
    print(*solution.flatten(), value)
