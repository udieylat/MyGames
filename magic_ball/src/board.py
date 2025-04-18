from dataclasses import dataclass

from magic_ball.src.models import PlayerSign


@dataclass
class InvalidMove(Exception):
    description: str


class Board:
    def __init__(self):
        self._board = self._init_board()

    def display(self):
        print()
        for row_i in range(4, -1, -1):
            print(' '.join([str(row_i + 1)] + self._board[row_i]))
        print("  A B C D E")
        print()

    def push(
        self,
        target_tile: str,
        player: PlayerSign,
    ):
        self._validate_tile(
            tile=target_tile,
        )
        col_i, row_i = self._tile_index(
            tile=target_tile,
        )
        target_board_tile = self._board[row_i][col_i]
        if target_board_tile != '.':
            raise InvalidMove(
                description=f"target tile not vacant: {target_board_tile}",
            )

        source_row_i = (
            row_i - 1
            if player == PlayerSign.white
            else row_i + 1
        )
        if not 0 <= source_row_i <= 4:
            raise InvalidMove(
                description=f"invalid source row index: {source_row_i}",
            )

        source_board_tile = self._board[source_row_i][col_i]
        if (
            (player == PlayerSign.white and source_board_tile != 'W')
            or (player == PlayerSign.black and source_board_tile != 'B')
        ):
            raise InvalidMove(
                description=(
                    f"source board tile is not a valid pawn: "
                    f"({source_row_i}, {col_i}) = {source_board_tile}"
                ),
            )

        # Complete push move.
        self._board[source_row_i][col_i] = '.'
        self._board[row_i][col_i] = (
            'W'
            if player == PlayerSign.white
            else 'B'
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

    @classmethod
    def _tile_index(
        cls,
        tile: str,
    ) -> tuple[int, int]:
        return (
            "ABCDE".index(tile[0]),
            "12345".index(tile[1]),
        )
