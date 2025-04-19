from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from models import PlayerSign, TileType
from move import Move


class Charge(Card):

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
        direction = (
            1
            if player_sign == PlayerSign.white
            else -1
        )
        move_indices: list[tuple[int, int, int]] = []
        for col_i, source_row_i in pawn_indices:
            target_row_i = source_row_i
            while True:
                target_row_i += direction
                if target_row_i == 0 or target_row_i == 4 or board[target_row_i][col_i] != TileType.vacant:
                    break
                move_indices.append((col_i, source_row_i, target_row_i))

        return [
            CardUtils.pawn_move(
                player_sign=player_sign,
                source_col_i=col_i,
                source_row_i=source_row_i,
                target_col_i=col_i,
                target_row_i=target_row_i,
                board=board,
                description=f"charge to target tile: {BoardUtils.indices_to_tile(col_i=col_i, row_i=target_row_i)}",
                card_index=card_index,
            )
            for col_i, source_row_i, target_row_i in move_indices
        ]
