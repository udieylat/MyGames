from dataclasses import dataclass

from models import PlayerSign, BallPosition


@dataclass
class Move:
    player_sign: PlayerSign
    result_board: list[list[str]]
    result_ball_position: BallPosition
    description: str
