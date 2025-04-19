import copy
from dataclasses import dataclass

from models import BallPosition, TileType
from move import Move


@dataclass
class InvalidMove(Exception):
    description: str



class Board:
    def __init__(self):
        self._board: list[list[str]] = self._init_board()
        self._ball_position: BallPosition = BallPosition.middle

    def __getitem__(self, item: int) -> list[str]:
        return self._board[item]

    def copy_board(self) -> list[list[str]]:
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
        print(f"{move.player_sign} play: {move.description}")
        self._board = move.result_board
        self._ball_position = move.result_ball_position

    @classmethod
    def _init_board(cls) -> list[list[str]]:
        board = [[TileType.vacant for _ in range(5)] for _ in range(5)]
        board[0] = [TileType.white for _ in range(5)]  # White pawns
        board[4] = [TileType.black for _ in range(5)]  # Black pawns
        return board

