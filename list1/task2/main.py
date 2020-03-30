from sys import stderr
from tabu_search import *

TABU_SIZE = 1000

if __name__ == '__main__':
    t, n = input().split()
    t = int(t)
    n = int(n)
    cities = np.ndarray((n, n))
    for i in range(n):
        for j, x in enumerate(input().split()):
            cities[i][j] = int(x)
    solution = TabuSearch(cities, t).tabu_search(TABU_SIZE)
    print(solution)
    print(solution.path, file=stderr)
