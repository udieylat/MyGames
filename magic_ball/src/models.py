from enum import StrEnum, IntEnum


class GameStatus(IntEnum):
    ongoing = 1
    white_win = 2
    black_win = 3
    draw = 4


class TileType(StrEnum):
    white = "W"
    black = "B"
    vacant = "."
    wall = "#"


class PlayerSign(StrEnum):
    white = "white"
    black = "black"


class BallPosition(StrEnum):
    white = "white"
    middle = "middle"
    black = "black"
