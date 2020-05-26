import numpy as np


class Agent:
    EMPTY = 0
    WALL = 1
    AGENT = 5
    EXIT = 8

    def __init__(self, board):
        self.board = board.copy()
        agent_position = np.where(board == Agent.AGENT)
        self.current_agent_position = [int(agent_position[0]), int(agent_position[1])]
        self.moves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1], 'H': [0, 0]}

    def look_down(self, directory):
        return int(
            self.board[self.current_agent_position[0] + self.moves[directory][0], self.current_agent_position[1] +
                       self.moves[directory][1]])

    def move(self, directory):
        direction = self.moves[directory]
        new_position = [self.current_agent_position[0] + direction[0], self.current_agent_position[1] + direction[1]]
        if self.look_down(directory) == Agent.EMPTY:
            self.board[new_position[0], new_position[1]] = Agent.AGENT
            self.board[self.current_agent_position[0], self.current_agent_position[1]] = Agent.EMPTY
            self.current_agent_position = new_position
        elif self.look_down(directory) == Agent.EXIT:
            self.board[self.current_agent_position[0], self.current_agent_position[1]] = Agent.EMPTY
            self.current_agent_position = new_position
        return directory
