from pydantic import BaseModel

from game_config import GameConfig
from models import PlayerSign


class SimulationSummary(BaseModel):
    config: GameConfig
    num_games: int
    num_white_wins: int
    num_draws: int
    num_black_wins: int
    runtime_sec: float = 0.0

    def white_win_percentage(self) -> float:
        return self.num_white_wins / self.num_games * 100

    def black_win_percentage(self) -> float:
        return self.num_black_wins / self.num_games * 100

    def win_percentage(self, player_sign: PlayerSign) -> float:
        return (
            self.white_win_percentage()
            if player_sign == PlayerSign.white
            else self.black_win_percentage()
        )
