from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Jump(Card):

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
        direction = (
            2
            if player_sign == PlayerSign.white
            else -2
        )
        move_indices = [
            (col_i, source_row_i, source_row_i + direction)
            for col_i, source_row_i in pawn_indices
            if 0 <= source_row_i + direction <= 4
            and board[source_row_i + direction][col_i] == TileType.vacant
        ]

        return [
            CardUtils.pawn_move(
                player_sign=player_sign,
                source_col_i=col_i,
                source_row_i=source_row_i,
                target_col_i=col_i,
                target_row_i=target_row_i,
                board=board,
                card_name=str(cls.name),
                card_index=card_index,
            )
            for col_i, source_row_i, target_row_i in move_indices
        ]
