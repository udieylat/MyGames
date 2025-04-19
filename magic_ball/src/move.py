from dataclasses import dataclass

from models import BoardType, PlayerSign, BallPosition


@dataclass
class Move:
    player_sign: PlayerSign
    result_board: BoardType
    result_ball_position: BallPosition
    description: str
