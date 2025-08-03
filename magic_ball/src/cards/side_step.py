from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move, CardMove


class SideStep(Card):

    @classmethod
    def description(cls) -> str:
        return "Moves a pawn sideways"

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
        move_indices: list[tuple[int, int, int]] = []
        for source_col_i, row_i in pawn_indices:
            for direction in [-1, 1]:
                target_col_i = source_col_i
                while True:
                    target_col_i += direction
                    if target_col_i == -1 or target_col_i == 5 or board[row_i][target_col_i] != TileType.vacant:
                        break
                    move_indices.append((source_col_i, target_col_i, row_i))

        return [
            CardUtils.pawn_move(
                player_sign=player_sign,
                source_col_i=source_col_i,
                source_row_i=row_i,
                target_col_i=target_col_i,
                target_row_i=row_i,
                board=board,
                card_name=str(cls.name),
                card_index=card_index,
            )
            for source_col_i, target_col_i, row_i in move_indices
        ]
