import numpy as np

EMPTY = 0
WALL = 1
AGENT = 5
EXIT = 8


class Agent:
    def __init__(self, board):
        agent_position = np.where(board == AGENT)
        self.board = board.copy()
        self.current_position = [int(agent_position[0]), int(agent_position[1])]

    def look(self, directory):
        return self._look(self._get_changes(directory))

    def go(self, directory):
        changes = self._get_changes(directory)
        neighbour = self._look(changes)
        new_position = [self.current_position[0] + changes[0], self.current_position[1] + changes[1]]
        if neighbour == EMPTY:
            self.board[self.current_position[0], self.current_position[1]] = EMPTY
            self.board[new_position[0], new_position[1]] = AGENT
            self.current_position = new_position
        elif neighbour == WALL:
            raise HitWallException
        elif neighbour == EXIT:
            self.board[self.current_position[0], self.current_position[1]] = EMPTY
            self.current_position = new_position
        return directory

    def _look(self, changes):
        return int(self.board[self.current_position[0] + changes[0],
                              self.current_position[1] + changes[1]])

    def _get_changes(self, directory):
        return self._changes[directory]

    _changes = {
        'U': [-1, 0],  # UP
        'D': [1, 0],   # DOWN
        'L': [0, -1],  # LEFT
        'R': [0, 1],   # RIGHT
        'H': [0, 0]    # HERE
    }


class HitWallException(Exception):
    pass
