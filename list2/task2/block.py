import random

import numpy as np


class Block:
    values = [0, 32, 64, 128, 160, 192, 223, 255]

    def __init__(self, array_width_position: int, array_height_position: int, width: int, height: int):
        self.array_width_position = array_width_position
        self.array_height_position = array_height_position
        self.width_position = width * array_width_position
        self.height_position = height * array_height_position
        self.width = width
        self.height = height
        self.value = random.choice(Block.values)
        self.widen = False
        self.higher = False
        self._distance = None

    def count_distance(self, data: np.array) -> int:
        if self._distance is not None:
            return self._distance
        self._distance = 0
        for i in range(self.height_position, self.height_position + self.height):
            for j in range(self.width_position, self.width_position + self.width):
                self._distance += (data[i][j] - self.value) ** 2
        return self._distance

    def clear_distance(self) -> None:
        self._distance = None

    def set_random_value(self):
        self.value = random.choice(Block.values)
        self._distance = None
