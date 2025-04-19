from __future__ import annotations

from board import InvalidMove, Board
from cards_randomizer import CardsRandomizer
from helper import Helper
from move import Move
from players.player import Player
from models import PlayerSign, GameStatus
from players.player_config import PlayerConfig, PlayerType
from players.player_factory import PlayerFactory


class GameManager:

    @classmethod
    def new(
        cls,
        white_player_config: PlayerConfig | None = None,
        black_player_config: PlayerConfig | None = None,
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
        )

    def __init__(
        self,
        white_player: Player,
        black_player: Player,
    ):
        assert white_player.player_sign == PlayerSign.white
        assert black_player.player_sign == PlayerSign.black
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._draw_cards()
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
            print("Game is already over.")
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
            print(f"** Invalid move: {e.description}")
            raise

        self._display()

    def show_card_available_moves(
        self,
        card_index: int,
    ):
        available_moves = self._get_card_available_moves(
            card_index=card_index,
        )
        print("Available moves:")
        for i, move in enumerate(available_moves):
            print(f" {i}. {move.description}")

    def play_card(
        self,
        card_index: int,
        move_index: int,
    ):
        if not self._game_on:
            print("Game is already over.")
            return

        available_moves = self._get_card_available_moves(
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
            print(f"** Invalid move: {e.description}")
            raise

    def pass_turn(self):
        if not self._game_on:
            print("Game is already over.")
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
            print("Cannot pass turn, there are available moves.")
        else:
            print("Pass turn, no available moves for player.")
            self._complete_turn()

    def _draw_cards(self):
        white_cards, black_cards = CardsRandomizer.draw_cards()
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
        print(f"{move.player_sign} play: {move.description}")
        self._board.play_move(
            move=move,
        )

    def _display(self):
        self._board.display()
        if self._game_on:
            print(f"Player turn: {self._player_turn}")

    def _complete_turn(self):
        self._player_turn = (
            PlayerSign.white
            if self._player_turn == PlayerSign.black
            else PlayerSign.black
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
                print("White wins!")
                self._game_on = False
            case GameStatus.black_win:
                print("Black wins!")
                self._game_on = False
            case GameStatus.draw:
                print("Game is drawn!")
                self._game_on = False

    def _get_card_available_moves(
        self,
        card_index: int,
    ) -> list[Move]:
        player = (
            self._white_player
            if self._player_turn == PlayerSign.white
            else self._black_player
        )
        return player.get_card_available_moves(
            card_index=card_index,
            board=self._board,
        )

    def _play_ai_player_turn_if_necessary(self):
        if not self._game_on:
            return

        player = (
            self._white_player
            if self._player_turn == PlayerSign.white
            else self._black_player
        )
        if player.is_human:
            return

        move = player.find_move(
            board=self._board,
        )
        self._play_move(
            move=move,
        )
        self._complete_turn()
