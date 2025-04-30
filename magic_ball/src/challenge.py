from __future__ import annotations

import random

from cards.cards_config import CardsConfig
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from game_config import GameConfig
from game_manager import GameManager
from models import PlayerSign
from players.player_config import PlayerConfig


class Challenge:
    def __init__(
        self,
        opponent_config: PlayerConfig = PlayerConfig.default_ai_opponent(),
        cards_config: CardsConfig = CardsConfig(),
    ):
        self._opponent_config = opponent_config
        self._cards_config = cards_config
        self._game_manager: GameManager | None = None
        self._level = 0

    def start(
        self,
        player_sign: PlayerSign | None = None,
    ) -> GameManager:
        self._game_manager = GameManager.new(
            config=self._to_game_config(
                player_sign=player_sign,
            ),
        )
        return self._game_manager

    def next_level(self):
        pass

    def _to_game_config(
        self,
        player_sign: PlayerSign | None,
    ) -> GameConfig:
        if player_sign is None:
            player_sign = random.choice(list(PlayerSign.__members__.keys()))

        cards_config = self._cards_config.model_copy()
        if player_sign == PlayerSign.white:
            white_player = PlayerConfig.human()
            black_player = self._opponent_config
            cards_config.num_white_cards = DEFAULT_NUM_CARDS_PER_PLAYER
            cards_config.num_black_cards = self._get_num_opponent_cards()
        else:
            white_player = self._opponent_config
            black_player = PlayerConfig.human()
            cards_config.num_white_cards = self._get_num_opponent_cards()
            cards_config.num_black_cards = DEFAULT_NUM_CARDS_PER_PLAYER

        return GameConfig(
            white_player=white_player,
            black_player=black_player,
            cards_config=cards_config,
        )

    def _get_num_opponent_cards(self) -> int:
        match self._level:
            case 0:
                return DEFAULT_NUM_CARDS_PER_PLAYER
            case 1:
                return 5
            case 2:
                return 7
            case _:
                return 10
