from __future__ import annotations

from magic_ball.src.board import Board, InvalidMove
from magic_ball.src.models import PlayerSign, PlayerType, BallPosition
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

        self._display()

    def __repr__(self) -> str:
        self._display()
        return ""

    def push(
        self,
        target_tile: str,
    ):
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
        move: str,
    ):
        # TODO
        pass

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
        # TODO: check end condition
        self._display()
        # TODO: what more?
