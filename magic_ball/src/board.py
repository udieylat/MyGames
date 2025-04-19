from dataclasses import dataclass

from helper import Helper
from models import BallPosition, GameStatus, PlayerSign, MoveType, TileType
from move import PossibleMoveType


@dataclass
class InvalidMove(Exception):
    description: str



class Board:
    def __init__(self):
        self._board = self._init_board()
        self._ball_position: BallPosition = BallPosition.middle

    def __getitem__(self, item: int) -> list[str]:
        return self._board[item]

    def get_game_status(
        self,
        white_magic_cards: list = [],
        black_magic_cards: list = [],  # TODO: impl once ready with magic cards
    ) -> GameStatus:
        if self._is_player_win(
            player_sign=PlayerSign.white,
        ):
            return GameStatus.white_win
        if self._is_player_win(
            player_sign=PlayerSign.black,
        ):
            return GameStatus.black_win
        if self._is_draw(
            white_magic_cards=white_magic_cards,
            black_magic_cards=black_magic_cards,
        ):  # TODO: impl also the defensive cards win condition
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
        col_i, row_i = Helper.tile_index(
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
        if not Helper.is_tile_player_pawn(
            player_sign=player,
            tile=source_board_tile,
        ):
            raise InvalidMove(
                description=(
                    f"source board tile is not a valid pawn: "
                    f"{Helper.indices_to_tile(col_i=col_i, row_i=source_row_i)} = {source_board_tile}"
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

    def _is_draw(
        self,
        white_magic_cards: list,
        black_magic_cards: list,
    ) -> bool:
        white_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.white,
            board=self._board,
        )
        black_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.black,
            board=self._board,
        )
        return not white_available_push_moves and not black_available_push_moves
