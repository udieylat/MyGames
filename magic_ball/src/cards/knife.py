from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign
from move import Move


class Knife(Card):

    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pawn_indices = Helper.get_pawn_indices(
            player_sign=player_sign,
            board=board,
        )
        neighbor_opponent_indices = [
            (col_i, row_i)
            for pawn_col_i, pawn_row_i in pawn_indices
            for col_i, row_i in BoardUtils.get_neighbor_tiles_indices(
                col_i=pawn_col_i,
                row_i=pawn_row_i,
            )
            if BoardUtils.is_tile_opponent_pawn(
                player_sign=player_sign,
                tile=board[row_i][col_i],
            )
        ]
        return [
            Move(
                player_sign=player_sign,
                result_board=Helper.eliminate_pawn(
                    col_i=col_i,
                    row_i=row_i,
                    board=board.copy_board(),
                ),
                result_ball_position=CardUtils.push_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=f"{cls.name}: {BoardUtils.indices_to_tile(col_i=col_i, row_i=row_i)}",
                used_card_index=card_index,
            )
            for col_i, row_i in neighbor_opponent_indices
        ]
