from __future__ import annotations

from cards.cards_config import CardsConfig
from cards.cards_randomizer import CardsRandomizer
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from game_config import GameConfig
from game_manager import GameManager
from game_simulator import GameSimulator
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
        self._challenge_card_names = self._set_challenge_card_names(
            challenge_card_names=challenge_card_names,
        )
        if self._player_sign == PlayerSign.white:
            self._cards_config = CardsConfig(
                white_card_names=self._challenge_card_names,
            )
        else:
            self._cards_config = CardsConfig(
                black_card_names=self._challenge_card_names,
            )
        self._game_manager: GameManager | None = None
        self._level = 0
        self._num_restarts = 0

    def start(self) -> GameManager:
        self.challenge_status()
        self._game_manager = GameManager.new(
            config=self._to_game_config(),
        )
        return self._game_manager

    def next_level(self) -> GameManager | None:
        if not self._game_is_won_by_human():
            print(f"Game is not won. Stay in level {self._level} and restart.")
            self._num_restarts += 1
            return self.start()

        self._level += 1
        if self._level == 4:
            print("YOU WON THE CHALLENGE!!!")
            print()
            print(f"Number of restarts: {self._num_restarts} ;)")
            return None

        print(f"LEVEL UP: {self._level}")
        return self.start()

    def simulate(
        self,
        num_games: int = 1000,
        level: int | None = None,
    ):
        if level is None:
            level = self._level
        simulator = GameSimulator(
            config=self._to_simulator_game_config(
                level=level,
            ),
        )
        simulation_summary = simulator.run(
            num_games=num_games,
        )
        win_percentage = simulation_summary.win_percentage(
            player_sign=self._player_sign,
        )
        print(f"Challenge simulation results over {num_games} games:")
        print(f" Level: {level or 0} ({self._get_num_opponent_cards(level=level)} cards for opponent)")
        print(f" Win percentage for {self._player_sign}: {win_percentage:.2f}%")
        print(f" Simulation runtime: {simulation_summary.runtime_sec:.2f} seconds")

    def simulate_win(
        self,
        level: int | None = None,
    ) -> GameManager:
        if level is None:
            level = self._level
        simulator = GameSimulator(
            config=self._to_simulator_game_config(
                level=level,
            ),
        )
        return simulator.find_first(
            winner_player_sign=self._player_sign,
        )

    def challenge_status(self):
        print(f"Level: {self._level}")
        print(f"Number of opponent cards: {self._get_num_opponent_cards(level=self._level)}")
        print(f"Playing as: {self._player_sign}")
        print("Challenge cards:")
        for i, card_name in enumerate(self._challenge_card_names):
            print(f" {i+1}. {card_name}")
        print(f"Number of restarts: {self._num_restarts}")
        print()

    def _set_challenge_card_names(
        self,
        challenge_card_names: list[str] | None,
    ) -> list[str]:
        if challenge_card_names is None:
            return self._randomize_challenge_cards()
        assert len(challenge_card_names) == DEFAULT_NUM_CARDS_PER_PLAYER, "Input challenge cards must be of size 3"
        return challenge_card_names

    def _to_game_config(self) -> GameConfig:
        cards_config = self._cards_config.model_copy()
        if self._player_sign == PlayerSign.white:
            white_player = PlayerConfig.human()
            black_player = self._opponent_config
            cards_config.num_white_cards = DEFAULT_NUM_CARDS_PER_PLAYER
            cards_config.num_black_cards = self._get_num_opponent_cards(level=self._level)
        else:
            white_player = self._opponent_config
            black_player = PlayerConfig.human()
            cards_config.num_white_cards = self._get_num_opponent_cards(level=self._level)
            cards_config.num_black_cards = DEFAULT_NUM_CARDS_PER_PLAYER

        return GameConfig(
            white_player=white_player,
            black_player=black_player,
            cards_config=cards_config,
        )

    def _to_simulator_game_config(
        self,
        level: int,
    ) -> GameConfig:
        cards_config = self._cards_config.model_copy()
        white_player = self._opponent_config
        black_player = self._opponent_config
        if self._player_sign == PlayerSign.white:
            cards_config.num_white_cards = DEFAULT_NUM_CARDS_PER_PLAYER
            cards_config.num_black_cards = self._get_num_opponent_cards(level=level)
        else:
            cards_config.num_white_cards = self._get_num_opponent_cards(level=level)
            cards_config.num_black_cards = DEFAULT_NUM_CARDS_PER_PLAYER
        return GameConfig(
            white_player=white_player,
            black_player=black_player,
            cards_config=cards_config,
        )

    @classmethod
    def _get_num_opponent_cards(
        cls,
        level: int,
    ) -> int:
        match level:
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
