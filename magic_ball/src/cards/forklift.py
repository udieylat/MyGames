from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move, CardMove


class Forklift(Card):

    @classmethod
    def description(cls) -> str:
        return "Change a pawn's location in a rotation axis of a friendly pawn"

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
        move_indices: list[tuple[int, int, int, int, PlayerSign]] = []
        for col_i, row_i in pawn_indices:
            all_neighbor_tiles_indices = BoardUtils.get_neighbor_tiles_indices(
                col_i=col_i,
                row_i=row_i,
            ) + BoardUtils.get_diagonal_neighbor_tiles_indices(
                col_i=col_i,
                row_i=row_i,
            )

            source_indices = [
                (source_col_i, source_row_i)
                for source_col_i, source_row_i in all_neighbor_tiles_indices
                if board[source_row_i][source_col_i] not in [TileType.vacant, TileType.wall]
            ]
            target_indices = [
                (target_col_i, target_row_i)
                for target_col_i, target_row_i in all_neighbor_tiles_indices
                if board[target_row_i][target_col_i] == TileType.vacant
            ]
            move_indices += [
                (
                    source_col_i, source_row_i, target_col_i, target_row_i,
                    BoardUtils.tile_to_player_sign(tile=board[source_row_i][source_col_i]),
                )
                for source_col_i, source_row_i in source_indices
                for target_col_i, target_row_i in target_indices
            ]

        return [
            CardMove(
                player_sign=player_sign,
                result_board=Helper.move_pawn(
                    player_sign=source_pawn_player_sign,
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
                tile_marker_1=BoardUtils.indices_to_tile(col_i=source_col_i, row_i=source_row_i),
                tile_marker_2=BoardUtils.indices_to_tile(col_i=target_col_i, row_i=target_row_i),
            )
            for source_col_i, source_row_i, target_col_i, target_row_i, source_pawn_player_sign in move_indices
        ]
