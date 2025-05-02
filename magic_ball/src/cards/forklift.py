from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Forklift(Card):

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
        direction_offsets = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        # TODO!
        move_indices = [
            (source_col_i, source_row_i, target_col_i, target_row_i)
            for col_i, source_row_i in opponent_pawn_indices
            if board[opponent_start_row_i][col_i] == TileType.vacant
        ]

        return [
            Move(
                player_sign=player_sign,  # TODO!
                result_board=Helper.move_pawn(
                    player_sign=player_sign,  # TODO!
                    source_col_i=source_col_i,
                    source_row_i=source_row_i,
                    target_col_i=target_col_i,
                    target_row_i=target_row_i,
                    board=board.copy_board(),
                ),
                result_ball_position=CardUtils.push_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=cls._describe_pawn_move(
                    source_col_i=source_col_i,
                    source_row_i=source_row_i,
                    target_col_i=target_col_i,
                    target_row_i=target_row_i,
                ),
                used_card_index=card_index,
            )
            for source_col_i, source_row_i, target_col_i, target_row_i in move_indices
        ]
