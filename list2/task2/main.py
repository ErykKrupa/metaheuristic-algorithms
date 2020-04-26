import math
import random
import sys
from copy import deepcopy
from time import time

import numpy as np

from division import Division

probability_configuration = 100
initial_temperature = 5_000
temperature_change_factor = 0.0001


def get_neighbour(division: Division) -> Division:
    neighbour_division = deepcopy(division)
    if random.choice([True, False]):
        neighbour_division.get_random_block().set_random_value()
        return neighbour_division
    else:
        block = neighbour_division.get_random_atypical_size_block()
        if block is None:
            return get_neighbour(division)
        else:
            neighbourhood = neighbour_division.get_neighbour_blocks(block, up_down=block.higher, left_right=block.widen)
            if neighbourhood:
                neighbour_division.change_size(random.choice(neighbourhood), block)
                return neighbour_division
            else:
                return get_neighbour(division)


def simulated_annealing(max_time, initial_division) -> Division:
    def probability_for_worse_solution():
        return 1 / (1 + math.e ** (probability_configuration * (new_distance - current_distance) / temperature))

    end_time = time() + max_time
    temperature = initial_temperature
    current_division = initial_division
    current_distance = current_division.count_distance()
    best_division = current_division
    best_distance = current_distance
    temperature_change = 1 - temperature_change_factor
    while time() < end_time:
        new_division = get_neighbour(current_division)
        new_distance = new_division.count_distance()
        temperature *= temperature_change
        if (new_distance < current_distance
                or (new_distance >= current_distance
                    and random.random() < probability_for_worse_solution())):
            current_division = new_division
            current_distance = current_division.count_distance()
            if current_distance < best_distance:
                best_division = current_division
                best_distance = current_distance

    return best_division


if __name__ == '__main__':
    t, n, m, k = input().split()
    t, n, m, k = float(t), int(n), int(m), int(k)
    matrix = np.array([input().split() for i in range(n)], np.uint8(1))
    Division.data = matrix
    result = simulated_annealing(t, Division(k))
    print(result.count_distance())
    print(result, file=sys.stderr)
