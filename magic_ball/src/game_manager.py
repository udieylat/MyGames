from __future__ import annotations

from board import InvalidMove, Board
from board_utils import BoardUtils
from cards.card import Card
from cards.cards_randomizer import CardsRandomizer
from helper import Helper
from move import Move
from players.player import Player, NoAvailableMoves
from models import PlayerSign, GameStatus
from players.player_config import PlayerConfig, PlayerType
from players.player_factory import PlayerFactory


class GameManager:

    @classmethod
    def new(
        cls,
        white_player_config: PlayerConfig | None = None,
        black_player_config: PlayerConfig | None = None,
        cards_pull: list[Card] | None = None,
    ) -> GameManager:
        if white_player_config is None:
            white_player_config = PlayerConfig(
                type=PlayerType.human,
            )
        if black_player_config is None:
            black_player_config = PlayerConfig(
                type=PlayerType.human,
            )
        return GameManager(
            white_player=PlayerFactory.generate_player(
                player_config=white_player_config,
                player_sign=PlayerSign.white,
            ),
            black_player=PlayerFactory.generate_player(
                player_config=black_player_config,
                player_sign=PlayerSign.black,
            ),
            cards_pull=cards_pull,
        )

    def __init__(
        self,
        white_player: Player,
        black_player: Player,
        cards_pull: list[Card] | None = None,
    ):
        assert white_player.player_sign == PlayerSign.white
        assert black_player.player_sign == PlayerSign.black
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._draw_cards(
            cards_pull=cards_pull,
        )
        self._player_turn: PlayerSign = PlayerSign.white

        self._game_on = True
        self._play_ai_player_turn_if_necessary()
        self._display()

    def __repr__(self) -> str:
        self._display()
        return ""

    def push(
        self,
        target_tile: str,
    ):
        if not self._game_on:
            self._print("Game is already over.")
            return
        try:
            self._play_move(
                move=Helper.generate_push_move(
                    player_sign=self._player_turn,
                    target_tile=target_tile,
                    board=self._board,
                ),
            )
            self._complete_turn()
        except InvalidMove as e:
            self._print(f"** Invalid move: {e.description}")
            raise

    def show_card_available_moves(
        self,
        card_index: int,
    ):
        available_moves = self._get_available_card_moves(
            card_index=card_index,
        )
        if not available_moves:
            self._print("No available moves.")
            return
        self._print("Available moves:")
        for i, move in enumerate(available_moves):
            self._print(f" {i}. {move.description}")

    def play_card(
        self,
        card_index: int,
        move_index: int,
    ):
        if not self._game_on:
            self._print("Game is already over.")
            return

        available_moves = self._get_available_card_moves(
            card_index=card_index,
        )
        if not 0 <= move_index < len(available_moves):
            raise InvalidMove(
                description=(
                    f"card index {card_index} has {len(available_moves)} valid moves, invalid index: {move_index}"
                ),
            )

        try:
            self._play_move(
                move=available_moves[move_index],
            )
            self._complete_turn()
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
        )
        if available_moves:
            self._print("Cannot pass turn, there are available moves.")
        else:
            self._print("Pass turn, no available moves for player.")
            self._complete_turn()

    @property
    def _verbose(self) -> bool:
        return self._white_player.is_human or self._black_player.is_human

    def _print(self, message: str):
        if self._verbose:
            print(message)

    def _draw_cards(
        self,
        cards_pull: list[Card] | None = None,
    ):
        white_cards, black_cards = CardsRandomizer.draw_cards(
            cards_pull=cards_pull,
        )
        self._white_player.draw_cards(
            cards=white_cards,
        )
        self._black_player.draw_cards(
            cards=black_cards,
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

    def _display(self):
        if not self._verbose:
            return
        self._board.display()
        if not self._game_on:
            return
        player = self._get_player()
        for i, card in enumerate(player.cards):
            index_str = "X" if card.already_used else f"{i}."
            suffix = " [D]" if card.is_defensive else ""
            self._print(f" {index_str} {card.__class__.__name__}{suffix}")
        self._print("")
        self._print(f"Player turn: {self._player_turn}")

    def _complete_turn(self):
        self._player_turn = BoardUtils.inverse_player_sign(
            player_sign=self._player_turn,
        )
        self._check_end_condition()
        self._play_ai_player_turn_if_necessary()

    def _check_end_condition(self):
        game_status = Helper.get_game_status(
            board=self._board,
            white_cards=self._white_player.cards,
            black_cards=self._black_player.cards,
        )
        match game_status:
            case GameStatus.white_win:
                self._print("White wins!")
                self._game_on = False
            case GameStatus.black_win:
                self._print("Black wins!")
                self._game_on = False
            case GameStatus.draw:
                self._print("Game is drawn!")
                self._game_on = False
            case GameStatus.white_defensive_win:
                self._print("White wins! (defensive)")
                self._game_on = False
            case GameStatus.black_defensive_win:
                self._print("Black wins! (defensive)")
                self._game_on = False

        # TODO: print both hands

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

    def _get_available_card_moves(
        self,
        card_index: int,
    ) -> list[Move]:
        assert 0 <= card_index <= 2, f"invalid card index: {card_index}"
        player = self._get_player()
        return player.cards[card_index].get_available_card_moves(
            player_sign=player.player_sign,
            board=self._board,
            card_index=card_index,
        )

    def _play_ai_player_turn_if_necessary(self):
        if not self._game_on:
            return

        player = self._get_player()
        if player.is_human:
            self._display()
            return

        try:
            move = player.find_move(
                board=self._board,
                num_unused_player_cards=self._get_num_unused_cards(
                    cards=self._get_player().cards,
                ),
                num_unused_opponent_cards=self._get_num_unused_cards(
                    cards=self._get_opponent().cards,
                ),
            )
            self._play_move(
                move=move,
            )
        except NoAvailableMoves:
            self._print("Skip player turn since there are no available moves.")

        self._complete_turn()

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
