from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Spawn(Card):

    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        allowed_rows = (
            [0, 1, 2]
            if player_sign == PlayerSign.white
            else [2, 3, 4]
        )
        vacant_indices = [
            (col_i, row_i)
            for col_i in range(5)
            for row_i in allowed_rows
            if board[row_i][col_i] == TileType.vacant
        ]
        return [
            Move(
                player_sign=player_sign,
                result_board=Helper.set_pawn_tile(
                    player_sign=player_sign,
                    col_i=col_i,
                    row_i=row_i,
                    board=board.copy_board(),
                ),
                result_ball_position=CardUtils.push_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=f"spawn a pawn tile at: {BoardUtils.indices_to_tile(col_i=col_i, row_i=row_i)}",
                used_card_index=card_index,
            )
            for col_i, row_i in vacant_indices
        ]
