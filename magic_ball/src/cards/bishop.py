from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from models import PlayerSign, TileType
from move import Move


class Bishop(Card):

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
        min_allowed_row = 0 if player_sign == PlayerSign.white else 1
        max_allowed_row = 3 if player_sign == PlayerSign.white else 4
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
                        or not min_allowed_row <= target_row_i <= max_allowed_row
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
                description=(
                    f"bishop move to target tile: {BoardUtils.indices_to_tile(col_i=target_col_i, row_i=target_row_i)}"
                ),
                card_index=card_index,
            )
            for source_col_i, source_row_i, target_col_i, target_row_i in move_indices
        ]
