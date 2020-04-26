import random
from typing import List, Optional

import numpy as np

from block import Block


class Division:
    data = None

    def __init__(self, min_block_size: int):
        self.height = np.size(Division.data, 0)
        self.width = np.size(Division.data, 1)
        self.min_block_size = min_block_size
        self.amount_of_blocks_in_width = self.width // min_block_size
        self.amount_of_blocks_in_height = self.height // min_block_size
        self.additional_width = self.width - min_block_size * self.amount_of_blocks_in_width
        self.additional_height = self.height - min_block_size * self.amount_of_blocks_in_height
        self.blocks = [[Block(w, h, min_block_size, min_block_size)
                        for w in range(self.amount_of_blocks_in_width)]
                       for h in range(self.amount_of_blocks_in_height)]
        if self.additional_width:
            for i in range(self.amount_of_blocks_in_height):
                block = self.blocks[i][-1]
                block.width = min_block_size + self.additional_width
                block.widen = True
        if self.additional_height:
            for block in self.blocks[-1]:
                block.height = min_block_size + self.additional_height
                block.higher = True

    def count_distance(self) -> float:
        distance = 0
        for row in self.blocks:
            for block in row:
                distance += block.count_distance(self.data)
        return distance / (self.height * self.width)

    def get_random_block(self) -> Block:
        return random.choice(random.choice(self.blocks))

    def get_random_atypical_size_block(self) -> Optional[Block]:
        atypical_size_blocks = [block for row in self.blocks for block in row if block.widen or block.higher]
        return random.choice(atypical_size_blocks) if atypical_size_blocks else None

    def get_neighbour_blocks(self, block: Block, left_right: bool = True, up_down: bool = True) -> List[Block]:
        neighbourhood = []
        x = block.array_width_position
        y = block.array_height_position
        if 0 <= x - 1 and left_right:
            neighbour = self.blocks[y][x - 1]
            if block.height == neighbour.height and block.height_position == neighbour.height_position:
                neighbourhood.append(neighbour)
        if x + 1 < self.amount_of_blocks_in_width and left_right:
            neighbour = self.blocks[y][x + 1]
            if block.height == neighbour.height and block.height_position == neighbour.height_position:
                neighbourhood.append(neighbour)
        if 0 <= y - 1 and up_down:
            neighbour = self.blocks[y - 1][x]
            if block.width == neighbour.width and block.width_position == neighbour.width_position:
                neighbourhood.append(neighbour)
        if y + 1 < self.amount_of_blocks_in_height and up_down:
            neighbour = self.blocks[y + 1][x]
            if block.width == neighbour.width and block.width_position == neighbour.width_position:
                neighbourhood.append(neighbour)
        return neighbourhood

    def change_size(self, lesser: Block, greater: Block) -> None:
        if lesser.width_position == greater.width_position and lesser.width == greater.width:
            lesser.height += self.additional_height
            greater.height -= self.additional_height
            lesser.higher = True
            greater.higher = False
            if lesser.height_position < greater.height_position:
                greater.height_position += self.additional_height
            else:
                lesser.height_position -= self.additional_height
        elif lesser.height_position == greater.height_position and lesser.height == greater.height:
            lesser.width += self.additional_width
            greater.width -= self.additional_width
            lesser.widen = True
            greater.widen = False
            if lesser.width_position < greater.width_position:
                greater.width_position += self.additional_width
            else:
                lesser.width_position -= self.additional_width
        else:
            raise Exception("Impossible to change size.")
        lesser.clear_distance()
        greater.clear_distance()

    def __str__(self) -> str:
        array_representation = np.empty((self.height, self.width), np.uint8(1))
        for row in self.blocks:
            for block in row:
                for i in range(block.height_position, block.height_position + block.height):
                    for j in range(block.width_position, block.width_position + block.width):
                        array_representation[i][j] = block.value
        self.array_representation = array_representation # todo wypieprzyć
        str_representation = ""
        for i, row in enumerate(array_representation):
            for j, value in enumerate(row):
                str_representation += f'{value}'
                if j + 1 != len(row):
                    str_representation += ' '
            if i + 1 != len(array_representation):
                str_representation += "\n"
        return str(str_representation)
