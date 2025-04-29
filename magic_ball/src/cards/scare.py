from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Scare(Card):

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
        opponent_pawn_indices = Helper.get_pawn_indices(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=player_sign,
            ),
            board=board,
        )
        opponent_start_row_i = (
            4
            if player_sign == PlayerSign.white
            else 0
        )
        move_indices = [
            (col_i, source_row_i, opponent_start_row_i)
            for col_i, source_row_i in opponent_pawn_indices
            if board[opponent_start_row_i][col_i] == TileType.vacant
        ]

        return [
            CardUtils.pawn_move(
                player_sign=BoardUtils.inverse_player_sign(
                    player_sign=player_sign,
                ),
                source_col_i=col_i,
                source_row_i=source_row_i,
                target_col_i=col_i,
                target_row_i=target_row_i,
                board=board,
                description=cls._describe_pawn_move(
                    source_col_i=col_i,
                    source_row_i=source_row_i,
                    target_col_i=col_i,
                    target_row_i=target_row_i,
                ),
                card_index=card_index,
            )
            for col_i, source_row_i, target_row_i in move_indices
        ]
