from board import Board
from board_utils import BoardUtils
from cards.card import Card
from models import PlayerSign
from move import Move


class Charge(Card):
    def _get_available_moves(
        self,
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
        Move(
            player_sign=player_sign,
            result_board=new_board,
            result_ball_position=board.ball_position,
            description=f"charge to target tile: {target_tile}",
        )
