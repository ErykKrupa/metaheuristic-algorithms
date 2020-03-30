class Path:
    def __init__(self, move_sequence):
        self.move_sequence = move_sequence

    def swap_cities(self, city1, city2):
        tmp = list(self.move_sequence)
        tmp[city1], tmp[city2] = tmp[city2], tmp[city1]
        return Path(tuple(tmp))

    def __eq__(self, other):
        return self.move_sequence == other.move_sequence

    def __hash__(self):
        return hash(self.move_sequence)

    def __str__(self):
        return ' '.join([str(i + 1) for i in self.move_sequence] + [str(self.move_sequence[0] + 1)])
