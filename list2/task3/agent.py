from collections import namedtuple
import numpy as np

EMPTY = 0
WALL = 1
AGENT = 5
EXIT = 8
X = -1

direction_actions = {'L': (0, -1), 'U': (-1, 0), 'R': (0, 1), 'D': (1, 0)}
directions = ['L', 'U', 'R', 'D']
Position = namedtuple('Position', ['row', 'column'])


class Agent:
    class WallException(Exception):
        pass

    def __init__(self, board: np.ndarray, marking=False):
        self.marking = marking
        self.board = board.copy()
        agent_position = np.where(board == AGENT)
        self.current_position: Position = Position(int(agent_position[0]), int(agent_position[1]))

    def look(self, direction):
        row_action, column_action = direction_actions[direction]
        return self.board[self.current_position.row + row_action][self.current_position.column + column_action]

    def move(self, direction, change_board=True):
        destination: int = self.look(direction)
        if destination == EMPTY or (not change_board and destination == AGENT):
            row_action, column_action = direction_actions[direction]
            if change_board:
                self.board[self.current_position.row][self.current_position.column] = X if self.marking else EMPTY
                self.board[self.current_position.row + row_action][self.current_position.column + column_action] = AGENT
            self.current_position: Position = \
                Position(self.current_position.row + row_action, self.current_position.column + column_action)
        elif destination == WALL:
            raise Agent.WallException()
        elif destination == EXIT:
            row_action, column_action = direction_actions[direction]
            self.current_position = \
                Position(self.current_position.row + row_action, self.current_position.column + column_action)
