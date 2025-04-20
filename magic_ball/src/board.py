from __future__ import annotations

import copy
from dataclasses import dataclass

from models import BoardType, BallPosition, TileType
from move import Move


@dataclass
class InvalidMove(Exception):
    description: str



class Board:

    @classmethod
    def new(cls) -> Board:
        return Board(
            board=cls._init_board(),
            ball_position=BallPosition.middle,
        )

    def __init__(
        self,
        board: BoardType,
        ball_position: BallPosition,
    ):
        self._board = board
        self._ball_position = ball_position

    def __getitem__(self, item: int) -> list[str]:
        return self._board[item]

    def clone(self) -> Board:
        return Board(
            board=self.copy_board(),
            ball_position=self._ball_position,
        )

    def copy_board(self) -> BoardType:
        return copy.deepcopy(self._board)

    @property
    def ball_position(self) -> BallPosition:
        return self._ball_position

    def display(self):
        print()
        for row_i in range(4, -1, -1):
            print(' '.join([str(row_i + 1)] + self._board[row_i]))
        print("  A B C D E")
        print()
        print(f"Ball position: {self._ball_position}")
        print()

    def play_move(
        self,
        move: Move,
    ):
        # TODO: consider adding the cards to the board, as they're part of the full state
        # TODO: then they could be set as "used" in this function
        self._board = move.result_board
        self._ball_position = move.result_ball_position

    @classmethod
    def _init_board(cls) -> BoardType:
        board = [[TileType.vacant for _ in range(5)] for _ in range(5)]
        board[0] = [TileType.white for _ in range(5)]  # White pawns
        board[4] = [TileType.black for _ in range(5)]  # Black pawns
        return board

