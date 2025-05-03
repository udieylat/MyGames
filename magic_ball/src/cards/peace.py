from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign
from move import Move


class Peace(Card):

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
        opponent_pawn_indices = Helper.get_pawn_indices(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=player_sign,
            ),
            board=board,
        )
        if not pawn_indices or not opponent_pawn_indices:
            return []

        farthest_player_pawn_row_i = (
            max(
                row_i
                for _, row_i in pawn_indices
            )
            if player_sign == PlayerSign.white
            else min(
                row_i
                for _, row_i in pawn_indices
            )
        )
        farthest_opponent_pawn_row_i = (
            min(
                row_i
                for _, row_i in opponent_pawn_indices
            )
            if player_sign == PlayerSign.white
            else max(
                row_i
                for _, row_i in opponent_pawn_indices
            )
        )
        indices_pairs_to_eliminate = [
            (player_pawn_col_i, player_pawn_row_i, opponent_pawn_col_i, opponent_pawn_row_i)
            for (player_pawn_col_i, player_pawn_row_i) in pawn_indices
            for (opponent_pawn_col_i, opponent_pawn_row_i) in opponent_pawn_indices
            if player_pawn_row_i == farthest_player_pawn_row_i
            and opponent_pawn_row_i == farthest_opponent_pawn_row_i
        ]

        return [
            Move(
                player_sign=player_sign,
                result_board=Helper.eliminate_pawn(
                    col_i=player_pawn_col_i,
                    row_i=player_pawn_row_i,
                    board=Helper.eliminate_pawn(
                        col_i=opponent_pawn_col_i,
                        row_i=opponent_pawn_row_i,
                        board=board.copy_board(),
                    ),
                ),
                result_ball_position=CardUtils.push_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=BoardUtils.describe_pawns_elimination_move(
                    card_name=str(cls.name),
                    player_pawn_col_i=player_pawn_col_i,
                    player_pawn_row_i=player_pawn_row_i,
                    opponent_pawn_col_i=opponent_pawn_col_i,
                    opponent_pawn_row_i=opponent_pawn_row_i,
                ),
                used_card_index=card_index,
            )
            for player_pawn_col_i, player_pawn_row_i, opponent_pawn_col_i, opponent_pawn_row_i in indices_pairs_to_eliminate
        ]
