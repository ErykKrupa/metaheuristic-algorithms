class Solution:
    def __init__(self, tsp_path, tsp_instance):
        self.path = tsp_path
        self.cost_table = tsp_instance.cities
        self._cost = None

    @staticmethod
    def get_solution(tsp_path, tsp_instance, given_cost):
        solution = Solution(tsp_path, tsp_instance)
        solution._cost = given_cost
        return solution

    @property
    def cost(self):
        if self._cost is not None:
            return self._cost

        total_cost = sum(
            self.cost_table[self.path.move_sequence[i]][self.path.move_sequence[i + 1]] for i
            in range(len(self.path.move_sequence) - 1))

        total_cost += self.cost_table[self.path.move_sequence[-1]][self.path.move_sequence[0]]
        self._cost = total_cost
        return total_cost

    def __hash__(self):
        return self.path.__hash__()

    def __eq__(self, other):
        return self.path.move_sequence == other.path.move_sequence

    def __str__(self):
        return f'{int(self.cost)}'
