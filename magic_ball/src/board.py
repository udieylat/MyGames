import copy
from dataclasses import dataclass

from board_utils import BoardUtils
from models import BallPosition, PlayerSign, TileType
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

    def _push(
        self,
        target_tile: str,
        player: PlayerSign,
    ):
        self._validate_tile(
            tile=target_tile,
        )
        col_i, row_i = BoardUtils.tile_index(
            tile=target_tile,
        )
        target_board_tile = self._board[row_i][col_i]
        if target_board_tile != TileType.vacant:
            raise InvalidMove(
                description=f"target tile {target_tile} not vacant: {target_board_tile}",
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
        if not BoardUtils.is_tile_player_pawn(
            player_sign=player,
            tile=source_board_tile,
        ):
            raise InvalidMove(
                description=(
                    f"source board tile is not a valid pawn: "
                    f"{BoardUtils.indices_to_tile(col_i=col_i, row_i=source_row_i)} = {source_board_tile}"
                ),
            )

        # Complete push move.
        self._board[source_row_i][col_i] = TileType.vacant
        self._board[row_i][col_i] = (
            TileType.white
            if player == PlayerSign.white
            else TileType.black
        )

    @classmethod
    def _init_board(cls) -> list[list[str]]:
        board = [[TileType.vacant for _ in range(5)] for _ in range(5)]
        board[0] = [TileType.white for _ in range(5)]  # White pawns
        board[4] = [TileType.black for _ in range(5)]  # Black pawns
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
