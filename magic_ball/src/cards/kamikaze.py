from board import Board
from board_utils import BoardUtils
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Kamikaze(Card):

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
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        indices_pairs_to_eliminate: list[tuple[int, int, int, int]] = []
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
                    ):
                        break

                    target_tile = board[target_row_i][target_col_i]
                    if target_tile == TileType.vacant:
                        continue
                    elif target_tile == TileType.wall or BoardUtils.is_tile_player_pawn(
                        player_sign=player_sign,
                        tile=target_tile,
                    ):
                        break
                    elif BoardUtils.is_tile_opponent_pawn(
                        player_sign=player_sign,
                        tile=target_tile,
                    ):
                        indices_pairs_to_eliminate.append((source_col_i, source_row_i, target_col_i, target_row_i))
                        break
                    assert RuntimeError("Shouldn't reach here")

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
