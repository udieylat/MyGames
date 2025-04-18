from dataclasses import dataclass

from magic_ball.src.models import PlayerSign


@dataclass
class InvalidMove(Exception):
    description: str


class Board:
    def __init__(self):
        self._board = self._init_board()

    def display(self):
        print("\nBoard:")
        for row in self._board:
            print(' '.join(row))
        print()

    def push(
        self,
        target_tile: str,
        player: PlayerSign,
    ):
        self._validate_tile(
            tile=target_tile,
        )


    @classmethod
    def _init_board(cls) -> list[list[str]]:
        board = [['.' for _ in range(5)] for _ in range(5)]
        board[0] = ['W', 'W', 'W', 'W', 'W']  # White pawns
        board[4] = ['B', 'B', 'B', 'B', 'B']  # Black pawns
        return board

    @classmethod
    def _validate_tile(
        cls,
        tile: str,
    ):
        try:
            assert len(tile) == 2
            assert tile[0] in "ABCDE"
            assert tile[1] in "12345"
        except AssertionError:
            raise InvalidMove(
                description=f"tile '{tile}' format is invalid",
            )