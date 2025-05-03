from __future__ import annotations

import json
import time

from game_config import GameConfig
from game_manager import GameManager
from models import PlayerSign
from simulation_summary import SimulationSummary


class GameSimulator:

    @classmethod
    def from_config_filename(
        cls,
        config_filename: str,
    ) -> GameSimulator:
        config = GameConfig.model_validate(json.load(open(config_filename)))
        return GameSimulator(
            config=config,
        )

    def __init__(
        self,
        config: GameConfig,
    ):
        self._config = config

    def clone_config(self) -> GameConfig:
        return self._config.model_copy()

    def run(
        self,
        num_games: int,
    ) -> SimulationSummary:
        summary = SimulationSummary(
            config=self._config,
            num_games=num_games,
            num_white_wins=0,
            num_draws=0,
            num_black_wins=0,
        )

        start_ts = time.time()
        for _ in range(num_games):
            gm = GameManager.new(
                config=self._config,
            )
            game_summary = gm.export_summary()
            match game_summary.winner:
                case "white":
                    summary.num_white_wins += 1
                case "black":
                    summary.num_black_wins += 1
                case "draw":
                    summary.num_draws += 1
                case _:
                    raise RuntimeError(f"Unexpected game summary winner value: {game_summary.winner}")

        summary.runtime_sec = time.time() - start_ts
        return summary

    def find_first(
        self,
        winner_player_sign: PlayerSign,
        max_num_games: int = 1000,
    ) -> GameManager | None:
        for _ in range(max_num_games):
            gm = GameManager.new(
                config=self._config,
            )
            match winner_player_sign, gm.export_summary().winner:
                case (PlayerSign.white, "white") | (PlayerSign.black, "black"):
                    return gm

        print(f"Couldn't find a winning game for {winner_player_sign} after {max_num_games} simulations.")
        return None
