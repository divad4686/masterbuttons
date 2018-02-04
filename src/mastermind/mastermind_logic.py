from enum import Enum
from collections import namedtuple


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5
    BLACK = 6


MoveResult = namedtuple('MoveResult', 'Black White')


def make_move(game_pattern, played_pattern):
    if len(game_pattern) != 4 or len(played_pattern) != 4:
        raise ValueError
    game_positions = list(game_pattern)
    moves = list(played_pattern)

    black = 0
    white = 0
    for index in range(0, 4):
        if game_positions[index] == moves[index]:
            black += 1
            game_positions[index] = moves[index] = None

    for move in moves:
        if move is not None and move in game_positions:
            white += 1
            game_positions.remove(move)

    return MoveResult(Black=black, White=white)
