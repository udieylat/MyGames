from dataclasses import dataclass

from models import BoardType, PlayerSign, BallPosition


@dataclass
class Move:
    player_sign: PlayerSign
    result_board: BoardType
    result_ball_position: BallPosition
    description: str
    used_card_index: int | None = None


@dataclass
class CardMove(Move):
    tile_marker_1: str | None = None
    tile_marker_2: str | None = None
