from time import time
import numpy as np


def local_search(function, neighbour_function, max_execution_time):
    end_time = time() + max_execution_time
    best_solution = _get_naive_solution()
    while time() < end_time:
        result = function(best_solution)
        neighbourhood = neighbour_function(best_solution)
        for neighbour in neighbourhood:
            neighbour_result = function(neighbour)
            if result > neighbour_result:
                best_solution = neighbour
                break
        else:
            return best_solution
    return best_solution


def _get_naive_solution():
    return list(np.random.uniform(-100, 100, 4))


def _happy_cat(x):
    norm = np.linalg.norm(x)
    return ((norm - 4) ** 2) ** 0.125 + 1 / 4 * (0.5 * norm ** 2 + sum((x_i for x_i in x))) + 1 / 2


def _get_neighbour_happy_cat(component):
    return component + np.random.uniform(-1, 1)


def _griewank(x):
    return 1 + 1 / 4000 * sum((x_i ** 2 for x_i in x)) - np.product(
        [np.cos(x_i / np.sqrt(i)) for i, x_i in enumerate(x, 1)])


def _get_neighbour_griewank(component):
    return component + abs(component) * np.random.uniform(-1, 1) * 2


def _get_neighbourhood(solution, neighbour_function, number_of_neighbours):
    return [[neighbour_function(item) for item in solution] for _ in range(number_of_neighbours)]


if __name__ == '__main__':
    t, b = input().split()
    t = float(t)
    best = local_search(_happy_cat if b == '0' else _griewank,
                        lambda solution: _get_neighbourhood(solution, _get_neighbour_happy_cat if b == '0'
                                                            else _get_neighbour_griewank, 500), t)
    print(f'{best[0]} {best[1]} {best[2]} {best[3]} {(_happy_cat if b == "0" else _griewank)(best)}')

