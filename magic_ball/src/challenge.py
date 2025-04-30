from __future__ import annotations

from cards.cards_config import CardsConfig
from game_manager import GameManager
from models import PlayerSign
from players.player_config import PlayerConfig, PlayerType, ScoreMultipliers


class Challenge:
    def __init__(
        self,
        opponent_config: PlayerConfig = PlayerConfig.default_ai_opponent(),
        cards_config: CardsConfig = CardsConfig(),
    ):
        self._opponent_config = opponent_config
        self._cards_config = cards_config

    def start(
        self,
        player_sign: PlayerSign | None = None,
    ) -> GameManager:
        player_config = PlayerConfig.human()
        return self._gm

    # def next_level(self) -> GameManager:
    #     if self._gm._game_status