import numpy as np
from abc import ABC
from time import time
from path import *
from solution import *


class TabuSearch(ABC):
    def __init__(self, cities, max_time):
        self.cities = cities
        self.cities_amount = len(cities)
        self.max_time = max_time

    def tabu_search(self, tabu_size):
        end_time = time() + self.max_time
        initial_solution = self._get_naive_solution()
        tabu = {}
        global_best = initial_solution
        counter = 0
        while time() < end_time:
            counter += 1
            neighbourhood = self._get_neighbourhood(global_best)
            local_best = None
            local_best_cost = global_best.cost
            for neighbour in (n for n in neighbourhood if n not in tabu.keys()):
                if neighbour.cost < local_best_cost:
                    local_best = neighbour
                    local_best_cost = neighbour.cost
            if local_best is None:
                continue
            global_best = local_best
            tabu[local_best] = (counter, local_best_cost)
            tabu = {k: (j, val) for k, (j, val) in tabu.items() if counter - tabu_size < j}
        return global_best

    def _get_naive_solution(self):
        random_sequence = tuple([0] + list(np.random.permutation(range(1, self.cities_amount))))
        return Solution(Path(random_sequence), self)

    def _get_neighbourhood(self, solution):
        neighbourhood = []
        for i in range(self.cities_amount):
            for j in range(self.cities_amount):
                if j > i > 0:
                    neighbour_path = solution.path.swap_cities(i, j)
                    neighbour_cost = self._compute_cost(solution.path, solution.cost, (i, j))
                    neighbourhood.append(Solution.get_solution(neighbour_path, self, neighbour_cost))
        return neighbourhood

    def _compute_cost(self, base_path, base_path_cost, *inversions):
        path = base_path.move_sequence
        path_length = len(path)
        for i, j in inversions:
            if abs(i - j) == 1:
                base_path_cost -= self.cities[path[i - 1]][path[i]] + \
                    self.cities[path[i]][path[j]] + \
                    self.cities[path[j]][path[(j + 1) % path_length]]
                base_path_cost += self.cities[path[i - 1]][path[j]] + \
                    self.cities[path[j]][path[i]] + \
                    self.cities[path[i]][path[(j + 1) % path_length]]
                return base_path_cost
            base_path_cost += - self.cities[path[i - 1]][path[i]] - \
                self.cities[path[i]][path[(i + 1) % path_length]] - \
                self.cities[path[j - 1]][path[j]] - \
                self.cities[path[j]][path[(j + 1) % path_length]] + \
                self.cities[path[i - 1]][path[j]] + \
                self.cities[path[j]][path[(i + 1) % path_length]] + \
                self.cities[path[j - 1]][path[i]] + \
                self.cities[path[i]][path[(j + 1) % path_length]]
            return base_path_cost
