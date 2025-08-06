from __future__ import annotations

import json

from board import InvalidMove, Board
from board_utils import BoardUtils
from cards.card import Card
from cards.cards_config import CardsConfig
from cards.cards_randomizer import CardsRandomizer
from cards.compendium import Compendium
from game_config import GameConfig
from game_summary import GameSummary
from helper import Helper
from move import Move, CardMove
from players.player import Player, NoAvailableMoves
from models import PlayerSign, GameStatus
from players.player_factory import PlayerFactory


class GameManager:

    @classmethod
    def new(
        cls,
        config: GameConfig = GameConfig(),
        webpage_mode: bool = False,
    ) -> GameManager:
        return GameManager(
            config=config,
            webpage_mode=webpage_mode,
        )

    @classmethod
    def from_config_filename(
        cls,
        config_filename: str,
    ) -> GameManager:
        config = GameConfig.model_validate(json.load(open(config_filename)))
        return GameManager.new(
            config=config,
        )

    def __init__(
        self,
        config: GameConfig,
        board: Board | None = None,
        player_turn: PlayerSign = PlayerSign.white,
        webpage_mode: bool = False,
    ):
        self._config = config
        self._board = board or Board.new()
        self._player_turn = player_turn
        self._webpage_mode = webpage_mode

        self._white_player = PlayerFactory.generate_player(
            player_config=config.white_player,
            player_sign=PlayerSign.white,
        )
        self._black_player = PlayerFactory.generate_player(
            player_config=config.black_player,
            player_sign=PlayerSign.black,
        )
        self._draw_cards(
            cards_config=self._config.cards_config,
        )

        self._game_status: GameStatus = GameStatus.ongoing
        self._game_log: list[str] = []
        self._play_ai_player_turn_if_necessary()  # Also displays board on human's turn.

    def __repr__(self) -> str:
        self._display()
        return ""

    # Properties for the app.py

    @property
    def board(self) -> Board:
        return self._board

    @property
    def player_turn(self) -> PlayerSign:
        return self._player_turn

    # General methods

    @property
    def game_config(self) -> GameConfig:
        return self._config

    @property
    def game_status(self) -> GameStatus:
        return self._game_status

    def push(
        self,
        target_tile: str,
    ) -> Move | None:
        if not self._game_on:
            self._print("Game is already over.")
            return None
        try:
            move = Helper.generate_push_move(
                player_sign=self._player_turn,
                target_tile=target_tile.upper(),
                board=self._board,
            )
            self._play_move(
                move=move,
            )
            return move
        except InvalidMove as e:
            self._print(f"** Invalid move: {e.description}")
            raise

    def show_possible_opponent_cards(self):
        used_opponent_card_names = [
            card.name
            for card in self._get_opponent().cards
            if card.already_used
        ]
        if len(used_opponent_card_names) == self._num_allowed_playable_cards():
            self._print(f"Opponent already played all of their allowed cards: {used_opponent_card_names}")
            return

        possible_opponent_card_names = [
            card_name
            for card_name in Compendium.get_cards_names()
            if card_name not in self._get_player().card_names
            and card_name not in used_opponent_card_names
        ]
        self._print(
            f"Opponent ({self._get_opponent().player_sign}) already played cards {used_opponent_card_names} "
            f"and has {self._num_allowed_playable_cards() - len(used_opponent_card_names)} more cards to play out of: "
        )
        for i, card_name in enumerate(possible_opponent_card_names):
            self._print(f" {i+1}. {card_name}")
        self._print(f"Opponent number of cards: {len(self._get_opponent().cards)}")

    def play_card(
        self,
        card_index: int,
        move_index: int | None = None,
    ) -> Move | None:
        if not self._game_on:
            self._print("Game is already over.")
            return None

        if move_index is None:
            # This is relevant only for local interpreter play, leaving it for now.
            self._show_card_available_moves(
                card_index=card_index,
            )
            return None

        available_card_moves = self.get_available_card_moves(
            card_index=card_index,
        )
        if not 0 <= move_index < len(available_card_moves):
            raise InvalidMove(
                description=(
                    f"card index {card_index} has {len(available_card_moves)} valid moves, invalid index: {move_index}"
                ),
            )

        try:
            move = available_card_moves[move_index]
            self._play_move(
                move=move,
            )
            return move
        except InvalidMove as e:
            self._print(f"** Invalid move: {e.description}")
            raise

    def pass_turn(self):
        if not self._game_on:
            self._print("Game is already over.")
            return

        available_moves = Helper.get_available_moves(
            player_sign=self._player_turn,
            board=self._board,
            cards=(
                self._white_player.cards
                if self._player_turn == PlayerSign.white
                else self._black_player.cards
            ),
            num_allowed_playable_cards=self._num_allowed_playable_cards(),
        )
        if available_moves:
            self._print("Cannot pass turn, there are available moves.")
        else:
            self._print("Pass turn, no available moves for player.")
            self._game_log.append("pass")
            self._complete_turn()

    def log(self):
        if self._game_status == GameStatus.ongoing:
            self._print_game_log()
            self._board.display()
        else:
            self._print_game_over_if_necessary(force=True)

    def export_summary(self) -> GameSummary:
        return GameSummary(
            white_cards=self._white_player.card_names,
            black_cards=self._black_player.card_names,
            is_white_defensive=self._white_player.is_defensive,
            is_black_defensive=self._black_player.is_defensive,
            winner=(
                "white"
                if self._game_status in [GameStatus.white_win, GameStatus.white_defensive_win]
                else "black"
                if self._game_status in [GameStatus.black_win, GameStatus.black_defensive_win]
                else "draw"
            ),
            num_white_moves=int(len(self._game_log)/2),
            final_ball_position=self._board.ball_position,
        )

    def rematch_keep_white(self) -> GameManager:
        return GameManager.new(
            config=self._config.clone_with_white_cards(
                white_card_names=self._white_player.card_names,
            ),
        )

    def rematch_keep_black(self) -> GameManager:
        return GameManager.new(
            config=self._config.clone_with_black_cards(
                black_card_names=self._black_player.card_names,
            ),
        )

    def rematch_keep_both(self) -> GameManager:
        return GameManager.new(
            config=self._config.clone_with_white_cards(
                white_card_names=self._white_player.card_names,
            ).clone_with_black_cards(
                black_card_names=self._black_player.card_names,
            ),
        )

    @property
    def _verbose(self) -> bool:
        return self._white_player.is_human or self._black_player.is_human

    @property
    def _game_on(self) -> bool:
        return self._game_status == GameStatus.ongoing

    def _print(self, message: str = ""):
        if self._verbose:
            print(message)

    def _draw_cards(
        self,
        cards_config: CardsConfig,
    ):
        white_card_names, black_card_names = CardsRandomizer.draw_cards(
            white_card_names=cards_config.white_card_names,
            black_card_names=cards_config.black_card_names,
            num_white_cards=cards_config.num_white_cards,
            num_black_cards=cards_config.num_black_cards,
            cards_pull=cards_config.cards_pull,
        )
        self._white_player.set_cards(
            cards=white_card_names,
        )
        self._black_player.set_cards(
            cards=black_card_names,
        )

    def _play_move(
        self,
        move: Move,
    ):
        self._print(f"{move.player_sign} play: {move.description}")
        if move.used_card_index is not None:
            player = self._get_player()
            player.cards[move.used_card_index].use_card()
        self._board.play_move(
            move=move,
        )
        self._game_log.append(move.description)
        self._complete_turn()

    def _display(self):
        if not self._verbose:
            return
        self._board.display()
        if not self._game_on:
            return
        self._display_player_cards(
            player=self._get_player(),
        )
        self._print("")
        self._print(f"Player turn: {self._player_turn}")

    @classmethod
    def _display_player_cards(
        cls,
        player: Player,
    ):
        for i, card in enumerate(player.cards):
            index_str = "X" if card.already_used else f"{i}."
            suffix = " [D]" if card.is_defensive else ""
            print(f" {index_str} {card.name}{suffix}")


    def _show_card_available_moves(
        self,
        card_index: int,
    ):
        available_card_moves = self.get_available_card_moves(
            card_index=card_index,
        )
        if not available_card_moves:
            self._print("No available moves.")
            return
        self._print("Available moves:")
        for i, move in enumerate(available_card_moves):
            self._print(f" {i}. {move.description}")

    def _complete_turn(self):
        self._player_turn = BoardUtils.inverse_player_sign(
            player_sign=self._player_turn,
        )
        self._game_status = Helper.get_game_status(
            board=self._board,
            player_turn=self._player_turn,
            white_cards=self._white_player.cards,
            black_cards=self._black_player.cards,
        )
        self._print_game_over_if_necessary()
        self._play_ai_player_turn_if_necessary()

    def _print_game_log(self):
        for i, (white_move, black_move) in enumerate(zip(self._game_log[::2], self._game_log[1::2])):
            print(f" {i+1}. {white_move} ; {black_move}")
        if len(self._game_log) % 2 == 1:
            print(f" {int(len(self._game_log)/2) + 1}. {self._game_log[-1]}")

    def _print_game_over_if_necessary(self, force: bool = False):
        if not self._verbose and not force:
            return

        match self._game_status:
            case GameStatus.white_win:
                print("\nWhite wins!")
            case GameStatus.black_win:
                print("\nBlack wins!")
            case GameStatus.draw:
                print("\nGame is drawn!")
            case GameStatus.white_defensive_win:
                print("\nWhite wins! (defensive)")
            case GameStatus.black_defensive_win:
                print("\nBlack wins! (defensive)")
            case GameStatus.ongoing:
                return

        # Final board position.
        self._print_game_log()
        self._board.display()

        # Display all cards at end of game.
        print()
        print("White cards:")
        self._display_player_cards(
            player=self._white_player,
        )
        print()
        print("Black cards:")
        self._display_player_cards(
            player=self._black_player,
        )

    def _get_player(self) -> Player:
        return (
            self._white_player
            if self._player_turn == PlayerSign.white
            else self._black_player
        )

    def _get_opponent(self) -> Player:
        return (
            self._white_player
            if self._player_turn == PlayerSign.black
            else self._black_player
        )

    def get_available_card_moves(
        self,
        card_index: int,
    ) -> list[CardMove]:
        assert 0 <= card_index <= self._num_allowed_playable_cards() - 1, f"invalid card index: {card_index}"
        player = self._get_player()
        return player.cards[card_index].get_available_card_moves(
            player_sign=player.player_sign,
            board=self._board,
            card_index=card_index,
        )

    def _num_allowed_playable_cards(self) -> int:
        return min(len(self._white_player.cards), len(self._black_player.cards))

    def _play_ai_player_turn_if_necessary(self):
        if not self._game_on or self._webpage_mode:
            return

        player = self._get_player()
        if player.is_human:
            self._display()
            return

        try:
            move = player.find_move(
                board=self._board,
                player_cards=self._get_player().cards,
                opponent_cards=self._get_opponent().cards,
            )
            self._play_move(
                move=move,
            )
        except NoAvailableMoves:
            self._print("Skip player turn since there are no available moves.")
            self.pass_turn()

    @classmethod
    def _get_num_unused_cards(
        cls,
        cards: list[Card],
    ) -> int:
        return len(
            [
                card
                for card in cards
                if not card.already_used
            ]
        )
