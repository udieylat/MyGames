from board import Board
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import CardMove


class Bishop(Card):

    @classmethod
    def description(cls) -> str:
        return "Moves a pawn diagonally"

    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[CardMove]:
        pawn_indices = Helper.get_pawn_indices(
            player_sign=player_sign,
            board=board,
        )
        direction_offsets = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        move_indices: list[tuple[int, int, int, int]] = []
        for source_col_i, source_row_i in pawn_indices:
            for col_i_offset, row_i_offset in direction_offsets:
                target_col_i = source_col_i
                target_row_i = source_row_i
                while True:
                    target_col_i += col_i_offset
                    target_row_i += row_i_offset
                    if (
                        not 0 <= target_col_i <= 4
                        or not 0 <= target_row_i <= 4
                        or board[target_row_i][target_col_i] != TileType.vacant
                    ):
                        break
                    move_indices.append((source_col_i, source_row_i, target_col_i, target_row_i))

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
