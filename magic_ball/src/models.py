from enum import StrEnum, IntEnum


class GameStatus(IntEnum):
    ongoing = 1
    white_win = 2
    black_win = 3
    draw = 4


class PlayerSign(StrEnum):
    white = "white"
    black = "black"


class PlayerType(StrEnum):
    human = "human"
    ai = "ai"


class BallPosition(StrEnum):
    white = "white"
    middle = "middle"
    black = "black"


class MoveType(StrEnum):
    push = "push"
    magic_card = "magic_card"