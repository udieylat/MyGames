from board import Board
from board_utils import BoardUtils
from cards.card import Card
from helper import Helper
from models import PlayerSign
from move import Move


class Charge(Card):
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
        move_indices = []

        return [
            cls._indices_to_move(
                player_sign=player_sign,
                col_i=col_i,
                row_i=row_i,
                board=board,
            )
            for col_i, row_i in move_indices
        ]

    @classmethod
    def _indices_to_move(
        cls,
        player_sign: PlayerSign,
        col_i: int,
        row_i: int,
        board: Board,
    ) -> Move:
        result_board = Helper.move_pawn(

        )
        return Move(
            player_sign=player_sign,
            result_board=new_board,
            result_ball_position=cls._push_ball(
                player_sign=player_sign,
                ball_position=board.ball_position,
            ),
            description=f"charge to target tile: {BoardUtils.indices_to_tile(row_i=row_i, col_i=col_i)}",
        )
