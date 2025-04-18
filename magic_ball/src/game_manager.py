from __future__ import annotations

from magic_ball.src.board import Board, InvalidMove
from magic_ball.src.models import PlayerSign, PlayerType, BallPosition
from magic_ball.src.move import Move
from magic_ball.src.player import Player


class GameManager:

    @classmethod
    def new(
        cls,
    ) -> GameManager:
        return GameManager(
            white_player=Player(player_type=PlayerType.human),
            black_player=Player(player_type=PlayerType.human),
        )

    def __init__(
        self,
        white_player: Player,
        black_player: Player,
    ):
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._player_turn: PlayerSign = PlayerSign.white
        self._ball_position: BallPosition = BallPosition.middle

        self._game_on = True
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
            self._board.push(
                target_tile=target_tile,
                player=self._player_turn,
            )
            self._complete_turn()
        except InvalidMove as e:
            print(f"** Invalid move: {e.description}")
            self._display()

    def play_magic_card(
        self,
        # TODO arg
    ):
        if not self._game_on:
            print("Game is already over.")
            return

        # TODO
        pass

    def pass_turn(self):
        if not self._game_on:
            print("Game is already over.")
            return

        available_moves = []  # TODO
        if available_moves:
            print("Cannot pass turn, there are available moves.")
        else:
            print("Pass turn, no available moves for player.")
            self._complete_turn()

    def _display(self):
        self._board.display()
        print(f"Ball position: {self._ball_position}")
        print()
        print(f"Player turn: {self._player_turn}")

    def _complete_turn(self):
        self._player_turn = (
            PlayerSign.white
            if self._player_turn == PlayerSign.black
            else PlayerSign.black
        )
        self._check_end_condition()
        # TODO: what more?
        # TODO: play AI nif necessary
        self._display()

    def _check_end_condition(self):
        if any(
            self._board[0][col_i] == 'B'
            for col_i in range(5)
        ):
            print("Black wins!")
            self._game_on = False
        elif any(
            self._board[4][col_i] == 'W'
            for col_i in range(5)
        ):
            print("White wins!")
            self._game_on = False
        elif self._no_available_moves():
            print("Game is drawn!")
            self._game_on = False

        # TODO: implement random strategy

    def _no_available_moves(self) -> bool:
        return (
            self._white_player.get_available_moves(
                board=self._board,
                ball_position=self._ball_position,
            ) == []
            and self._black_player.get_available_moves(
                board=self._board,
                ball_position=self._ball_position,
            ) == []
        )
