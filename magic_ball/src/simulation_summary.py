from pydantic import BaseModel

from game_config import GameConfig


class SimulationSummary(BaseModel):
    config: GameConfig
    num_games: int
    num_white_wins: int
    num_draws: int
    num_black_wins: int
    runtime_sec: float = 0.0
