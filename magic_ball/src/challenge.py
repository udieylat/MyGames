from __future__ import annotations

from cards.cards_config import CardsConfig
from cards.cards_randomizer import CardsRandomizer
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from game_config import GameConfig
from game_manager import GameManager
from models import PlayerSign, GameStatus
from players.player_config import PlayerConfig


class Challenge:
    def __init__(
        self,
        player_sign: PlayerSign = PlayerSign.white,
        opponent_config: PlayerConfig = PlayerConfig.default_ai_opponent(),
        challenge_card_names: list[str] | None = None,
    ):
        self._player_sign = player_sign
        self._opponent_config = opponent_config

        if challenge_card_names is None:
            challenge_card_names = self._randomize_challenge_cards()
        else:
            assert len(challenge_card_names) == DEFAULT_NUM_CARDS_PER_PLAYER, "Input challenge cards must be of size 3"

        if self._player_sign == PlayerSign.white:
            self._cards_config = CardsConfig(
                white_card_names=challenge_card_names,
            )
        else:
            self._cards_config = CardsConfig(
                black_card_names=challenge_card_names,
            )
        self._game_manager: GameManager | None = None
        self._level = 0

    def start(self) -> GameManager:
        self._game_manager = GameManager.new(
            config=self._to_game_config(),
        )
        return self._game_manager

    def next_level(self) -> GameManager | None:
        if not self._game_is_won_by_human():
            print(f"Game is not won. Stay in level {self._level} and restart.")
            return self.start()

        self._level += 1
        if self._level == 4:
            print("YOU WON THE CHALLENGE!!!")
            return None

        print(f"LEVEL UP: {self._level}")
        return self.start()

    def challenge_status(self):
        print(f"Level: {self._level}")
        print(f"Number of opponent cards: {self._get_num_opponent_cards()}")
        print(f"Playing as: {self._player_sign}")
        print("Challenge cards:")
        card_names = (
            self._cards_config.white_card_names
            if self._player_sign == PlayerSign.white
            else self._cards_config.black_card_names
        )
        for i, card_name in enumerate(card_names):
            print(f" {i+1}. {card_name}")

    def _to_game_config(self) -> GameConfig:
        cards_config = self._cards_config.model_copy()
        if self._player_sign == PlayerSign.white:
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

    def _game_is_won_by_human(self) -> bool:
        if (
            self._player_sign == PlayerSign.white
            and self._game_manager.game_status in [GameStatus.white_win, GameStatus.white_defensive_win]
        ):
            return True
        if (
            self._player_sign == PlayerSign.black
            and self._game_manager.game_status in [GameStatus.black_win, GameStatus.black_defensive_win]
        ):
            return True

        return False

    @classmethod
    def _randomize_challenge_cards(cls) -> list[str]:
        cards, _ = CardsRandomizer.draw_cards()
        return [
            card.name
            for card in cards
        ]
