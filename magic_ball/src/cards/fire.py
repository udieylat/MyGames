from board import Board
from cards.card import Card
from cards.card_utils import CardUtils
from helper import Helper
from models import PlayerSign, TileType
from move import Move


class Fire(Card):

    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        allowed_rows = (
            [0, 1, 2]
            if player_sign == PlayerSign.white
            else [2, 3, 4]
        )
        return [
            cls._fire_row_to_move(
                row_i=row_i,
                player_sign=player_sign,
                board=board,
                card_index=card_index,
            )
            for row_i in allowed_rows
            if not cls._row_is_vacant(
                row_i=row_i,
                board=board,
            )
        ]

    @classmethod
    def _fire_row_to_move(
        cls,
        row_i: int,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> Move:
        result_board = board.copy_board()
        for col_i in range(5):
            result_board = Helper.eliminate_pawn(
                col_i=col_i,
                row_i=row_i,
                board=result_board,
                safe=True,  # Don't break if the tile is vacant
            )
        return Move(
            player_sign=player_sign,
            result_board=result_board,
            result_ball_position=CardUtils.push_ball(
                player_sign=player_sign,
                ball_position=board.ball_position,
            ),
            description=f"{cls.name} in row: {row_i}",
            used_card_index=card_index,
        )

    @classmethod
    def _row_is_vacant(
        cls,
        row_i: int,
        board: Board,
    ) -> bool:
        return all(
            board[row_i][col_i] == TileType.vacant
            for col_i in range(5)
        )
