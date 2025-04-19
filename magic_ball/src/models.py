from enum import StrEnum, IntEnum


BoardType = list[list[str]]


class GameStatus(IntEnum):
    ongoing = 1
    white_win = 2
    black_win = 3
    draw = 4
    white_defensive_win = 5
    black_defensive_win = 6


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
