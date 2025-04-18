from enum import StrEnum


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