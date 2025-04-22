from pydantic import BaseModel

from models import BallPosition


class GameSummary(BaseModel):
    white_cards: list[str]
    black_cards: list[str]
    is_white_defensive: bool
    is_black_defensive: bool
    winner: str  # white / black / draw
    num_white_moves: int
    final_ball_position: BallPosition
