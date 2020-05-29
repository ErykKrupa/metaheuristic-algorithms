import fileinput
import math
import random
import sys
import time
from copy import deepcopy, copy

import numpy as np

from agent import Agent, EXIT, directions, Position

initial_temperature = 5000
temperature_change_factor = 0.001


class Path(list):
    @property
    def steps(self) -> int:
        return len(self)

    def inversion(self, i, j) -> None:
        self[i], self[j] = self[j], self[i]

    def __hash__(self):
        return hash(tuple(self))


def validate(path: Path, agent=None):
    if agent is None:
        walker = Agent(board)
    else:
        walker = agent
    for i, direction in enumerate(path, 1):
        try:
            walker.move(direction, change_board=False)
            if board[walker.current_position.row, walker.current_position.column] == EXIT:
                return Path(path[:i]), True
        except Agent.WallException:
            return None, False
    return None, False


def get_random_neighbour(path: Path) -> Path:
    walker = Agent(board)
    walker_start_pos: Position = walker.current_position
    while True:
        walker.current_position = walker_start_pos
        path_copy = copy(path)
        suffix_end = np.random.randint(0, len(path_copy) - 1)
        path_copy[suffix_end:] = np.random.choice(directions, len(path_copy) - suffix_end)
        new_path, is_valid = validate(path_copy, agent=walker)
        if is_valid:
            return new_path


def simulated_annealing(max_time):
    def probability_for_worse_solution():
        return math.e ** (-delta / temperature)

    end_time = time.time() + max_time
    temperature = initial_temperature
    walker = Agent(board)
    walker_start: Position = walker.current_position
    while True:
        random_path = Path(np.random.choice(directions, size=board.size))
        walker.current_position = walker_start
        current_solution, is_valid = validate(random_path, agent=walker)
        if is_valid:
            break
    working_solution = deepcopy(current_solution)
    best_solution = deepcopy(current_solution)
    temperature_change = 1 - temperature_change_factor
    while time.time() < end_time:
        neighbour = get_random_neighbour(working_solution)
        delta = neighbour.steps - current_solution.steps
        if delta <= 0 or probability_for_worse_solution() > random.random():
            current_solution = deepcopy(neighbour)
            if neighbour.steps < best_solution.steps:
                best_solution = deepcopy(neighbour)
        temperature *= temperature_change
    return best_solution


if __name__ == '__main__':
    max_time, rows, columns = input().split()
    max_time, rows, columns = int(max_time), int(rows), int(columns)
    board = np.array([[int(char) for char in input()] for i in range(0, rows)])
    solution = simulated_annealing(max_time)
    print(''.join(solution), file=sys.stderr)
    print(solution.steps)
