from __future__ import annotations

import random

from cards.cards_config import CardsConfig
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from game_config import GameConfig
from game_manager import GameManager
from models import PlayerSign, GameStatus
from players.player_config import PlayerConfig, PlayerType


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
        # TODO: lock challenge hand (and sign??)

    def start(
        self,
        player_sign: PlayerSign | None = None,
    ) -> GameManager:
        # TODO: keep hand, also keep sign??
        self._game_manager = GameManager.new(
            config=self._to_game_config(
                player_sign=player_sign,
            ),
        )
        return self._game_manager

    def next_level(self) -> GameManager | None:
        # TODO: keep hand, also keep sign??
        if not self._game_is_won_by_human():
            print(f"Game is not won. Stay in level {self._level} and restart.")
            return self.start()

        self._level += 1
        if self._level == 4:
            print("YOU WON THE CHALLENGE!!!")

        print(f"LEVEL UP: {self._level}")
        return self.start()

    def my_level(self):
        print(f"Level: {self._level}")
        print(f"Number of opponent cards: {self._get_num_opponent_cards()}")

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
            # cards_config.white_card_names = [...]
        else:
            white_player = self._opponent_config
            black_player = PlayerConfig.human()
            cards_config.num_white_cards = self._get_num_opponent_cards()
            cards_config.num_black_cards = DEFAULT_NUM_CARDS_PER_PLAYER
            # cards_config.black_card_names = [...]

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

    def _game_is_won_by_human(self) -> bool:
        if (
            self._game_manager.game_config.white_player.type == PlayerType.human
            and self._game_manager.game_status in [GameStatus.white_win, GameStatus.white_defensive_win]
        ):
            return True
        if (
            self._game_manager.game_config.black_player.type == PlayerType.human
            and self._game_manager.game_status in [GameStatus.black_win, GameStatus.black_defensive_win]
        ):
            return True

        return False
