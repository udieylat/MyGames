from board import Board
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Tank(Card):

    @classmethod
    def description(cls) -> str:
        return "Creates an indestructible pawn"

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
        tank_move_indices = [
            (pawn_col_i, pawn_row_i, target_col_i, target_row_i, neighbor_target_col_i, neighbor_target_row_i)
            for pawn_col_i, pawn_row_i in pawn_indices
            for target_col_i, target_row_i, neighbor_target_col_i, neighbor_target_row_i in cls._get_tank_target_move_indices(
                pawn_col_i=pawn_col_i,
                pawn_row_i=pawn_row_i,
            )
            if board[target_row_i][target_col_i] != TileType.vacant  # Must push some non-vacant tile
            and board[neighbor_target_row_i][neighbor_target_col_i] == TileType.vacant  # Target tile must be vacant
        ]
        return [
            Move(
                player_sign=player_sign,
                result_board=Helper.move_tile(
                    source_col_i=source_col_i,
                    source_row_i=source_row_i,
                    target_col_i=target_col_i,
                    target_row_i=target_row_i,
                    board=Helper.move_tile(
                        source_col_i=target_col_i,
                        source_row_i=target_row_i,
                        target_col_i=neighbor_target_col_1,
                        target_row_i=neighbor_target_row_1,
                        board=board.copy_board(),
                    ),
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
            for source_col_i, source_row_i, target_col_i, target_row_i, neighbor_target_col_1, neighbor_target_row_1
            in tank_move_indices
        ]

    @classmethod
    def _get_tank_target_move_indices(
        cls,
        pawn_col_i: int,
        pawn_row_i: int,
    ) -> list[tuple[int, int, int, int]]:
        all_neighbor_tiles_indices = [
            (pawn_col_i, pawn_row_i + 1, pawn_col_i, pawn_row_i + 2),
            (pawn_col_i, pawn_row_i - 1, pawn_col_i, pawn_row_i - 2),
            (pawn_col_i + 1, pawn_row_i, pawn_col_i + 2, pawn_row_i),
            (pawn_col_i - 1, pawn_row_i, pawn_col_i - 2, pawn_row_i),
        ]
        return [
            indices
            for indices in all_neighbor_tiles_indices
            if all(
                0 <= index <= 4
                for index in indices
            )
        ]
