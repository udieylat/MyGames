from dataclasses import dataclass
from enum import StrEnum

from magic_ball import PlayerSign, BallPosition, MoveType, GameStatus
from magic_ball import PossibleMoveType


@dataclass
class InvalidMove(Exception):
    description: str


class TileType(StrEnum):
    white = "W"
    black = "B"
    vacant = "."
    wall = "#"


class Board:
    def __init__(self):
        self._board = self._init_board()
        self._ball_position: BallPosition = BallPosition.middle

    def __getitem__(self, item: int) -> list[str]:
        return self._board[item]

    def get_game_status(self) -> GameStatus:
        if self._is_player_win(
            player_sign=PlayerSign.white,
        ):
            return GameStatus.white_win
        if self._is_player_win(
            player_sign=PlayerSign.black,
        ):
            return GameStatus.black_win
        if self._is_draw():  # TODO: impl also the defensive cards win condition
            return GameStatus.draw
        return GameStatus.ongoing

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
        move: PossibleMoveType,
    ):
        match move.type:
            case MoveType.push:
                self._push(
                    target_tile=move.target_tile,
                    player=move.player_sign,
                )
            case MoveType.magic_card:
                # TODO
                pass

        # TODO: end turn

    def _push(
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
        if not self._is_tile_player_pawn(
            player_sign=player,
            tile=source_board_tile,
        ):
            raise InvalidMove(
                description=(
                    f"source board tile is not a valid pawn: "
                    f"{self._indices_to_tile(col_i=col_i, row_i=source_row_i)} = {source_board_tile}"
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

    @classmethod
    def _tile_index(
        cls,
        tile: str,
    ) -> tuple[int, int]:
        return (
            "ABCDE".index(tile[0]),
            "12345".index(tile[1]),
        )

    @classmethod
    def _indices_to_tile(
        cls,
        col_i: int,
        row_i: int,
    ) -> str:
        return "ABCDE"[col_i] + "12345"[row_i]

    @classmethod
    def _is_tile_player_pawn(
        cls,
        player_sign: PlayerSign,
        tile: str,
    ) -> bool:
        return (
            (player_sign == PlayerSign.white and tile == TileType.white)
            or (player_sign == PlayerSign.black and tile == TileType.black)
        )

    def _is_player_win(
        self,
        player_sign: PlayerSign,
    ) -> bool:
        if player_sign == PlayerSign.white:
            return any(
                self._board[4][col_i] == TileType.white
                for col_i in range(5)
            )
        return any(
            self._board[0][col_i] == TileType.black
            for col_i in range(5)
        )
