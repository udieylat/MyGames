from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from models import PlayerSign, TileType, BoardType
from move import Move


class Wall(Card):

    @property
    def is_defensive(self) -> bool:
        return True

    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pawn_indices = CardUtils.get_pawn_indices(
            player_sign=player_sign,
            board=board,
        )
        neighbor_vacant_indices = [
            (col_i, row_i)
            for pawn_col_i, pawn_row_i in pawn_indices
            for col_i, row_i in BoardUtils.get_neighbor_tiles_indices(
                col_i=pawn_col_i,
                row_i=pawn_row_i,
            )
            if board[row_i][col_i] == TileType.vacant
        ]

        return [
            Move(
                player_sign=player_sign,
                result_board=cls._put_wall_tile(
                    col_i=col_i,
                    row_i=row_i,
                    board=board.copy_board(),
                ),
                result_ball_position=CardUtils.push_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=f"put a wall tile at: {BoardUtils.indices_to_tile(col_i=col_i, row_i=row_i)}",
                used_card_index=card_index,
            )
            for col_i, row_i in neighbor_vacant_indices
        ]

    @classmethod
    def _put_wall_tile(
        cls,
        col_i: int,
        row_i: int,
        board: BoardType,
    ) -> BoardType:
        board[row_i][col_i] = TileType.wall
        return board
