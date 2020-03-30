from time import time
from random import randrange
from sys import stderr
from agent import *
from tabu import *

TABU_SIZE = 5


def tabu_search(seconds, board, tabu_size):
    end_time = time() + seconds
    naive_way = _get_naive_way(board)
    best_way = naive_way
    tabu = Tabu(tabu_size)
    tabu.push(naive_way)
    while time() < end_time:
        neighbourhood = _get_neighbourhood(best_way, tabu_size)
        neighbourhood = [_minimalize_way(i, board) for i in neighbourhood]
        for neighbour in neighbourhood:
            if not tabu.contains(neighbour) and _cost(neighbour) < _cost(best_way):
                best_way = neighbour
        tabu.push(best_way)
    return best_way


def _get_naive_way(board):
    agent = Agent(board)
    directions = ['L', 'U', 'R', 'D']
    way = []
    for i in range(-3, 3):
        side = directions[i - 1]
        front = directions[i]
        while True:
            if agent.look(side) == EXIT:
                way.append(agent.go(side))
                return way
            elif agent.look(front) == EMPTY:
                way.append(agent.go(front))
            else:
                break


def _get_neighbourhood(way, amount):
    length = len(way)
    neighbourhood = []
    for _ in range(amount):
        neighbour = way.copy()
        for _ in range(length):
            step1 = randrange(length)
            step2 = randrange(length)
            neighbour[step1], neighbour[step2] = neighbour[step2], neighbour[step1]
        neighbourhood.append(neighbour)
    return neighbourhood


def _minimalize_way(way, board):
    agent = Agent(board)
    for i, step in enumerate(way, start=1):
        try:
            agent.go(step)
        except HitWallException:
            return None
        else:
            if agent.look('H') == EXIT:
                return way[:i]
    return None


def _cost(way):
    return 1_000_000_000_000_000 if way is None else len(way)


if __name__ == '__main__':
    t, n, m = input().split()
    t = float(t)
    n = int(n)
    m = int(m)
    result = tabu_search(t, np.array([[int(char) for char in input()] for i in range(0, n)]), TABU_SIZE)
    print(len(result))
    print(''.join(result), file=stderr)
