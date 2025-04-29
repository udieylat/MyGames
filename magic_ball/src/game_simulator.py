from game_config import GameConfig
from game_manager import GameManager


class GameSimulator:
    def __init__(
        self,
        config: GameConfig,
    ):
        self._config = config

    def run(
        self,
        num_games: int,
    ):
        for _ in range(num_games):
            gm = GameManager.new(
                config=self._config,
            )
            gm.export_summary()
            # TODO
