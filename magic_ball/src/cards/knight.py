from board import Board
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Knight(Card):

    @classmethod
    def description(cls) -> str:
        return "Moves a pawn in L-shape pattern"

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
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2),
        ]
        move_indices = [
            (source_col_i, source_row_i, source_col_i + col_i_offset, source_row_i + row_i_offset)
            for source_col_i, source_row_i in pawn_indices
            for col_i_offset, row_i_offset in direction_offsets
            if 0 <= source_col_i + col_i_offset <= 4
            and 0 <= source_row_i + row_i_offset <= 4
            and board[source_row_i + row_i_offset][source_col_i + col_i_offset] == TileType.vacant
        ]

        return [
            CardUtils.pawn_move(
                player_sign=player_sign,
                source_col_i=source_col_i,
                source_row_i=source_row_i,
                target_col_i=target_col_i,
                target_row_i=target_row_i,
                board=board,
                card_name=str(cls.name),
                card_index=card_index,
            )
            for source_col_i, source_row_i, target_col_i, target_row_i in move_indices
        ]
