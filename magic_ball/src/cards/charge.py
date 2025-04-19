from board import Board
from board_utils import BoardUtils
from cards.card import Card
from helper import Helper
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
        pawn_indices: list[tuple[int, int]] = [
            (col_i, row_i)
            for col_i in range(5)
            for row_i in range(5)
            if BoardUtils.is_tile_player_pawn(
                player_sign=player_sign,
                tile=board[row_i][col_i],
            )
        ]
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
            cls._indices_to_move(
                player_sign=player_sign,
                col_i=col_i,
                source_row_i=source_row_i,
                target_row_i=target_row_i,
                board=board,
                card_index=card_index,
            )
            for col_i, source_row_i, target_row_i in move_indices
        ]

    @classmethod
    def _indices_to_move(
        cls,
        player_sign: PlayerSign,
        col_i: int,
        source_row_i: int,
        target_row_i: int,
        board: Board,
        card_index: int,
    ) -> Move:
        result_board = Helper.move_pawn(
            player_sign=player_sign,
            source_col_i=col_i,
            source_row_i=source_row_i,
            target_col_i=col_i,
            target_row_i=target_row_i,
            board=board.copy_board(),
        )
        return Move(
            player_sign=player_sign,
            result_board=result_board,
            result_ball_position=cls._push_ball(
                player_sign=player_sign,
                ball_position=board.ball_position,
            ),
            description=f"charge to target tile: {BoardUtils.indices_to_tile(row_i=target_row_i, col_i=col_i)}",
            used_card_index=card_index,
        )
