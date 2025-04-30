from board import Board
from helper import Helper
from models import PlayerSign, BallPosition
from move import Move


class CardUtils:
    @classmethod
    def pawn_move(
        cls,
        player_sign: PlayerSign,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
        board: Board,
        description: str,
        card_index: int,
    ) -> Move:
        result_board = Helper.move_pawn(
            player_sign=player_sign,
            source_col_i=source_col_i,
            source_row_i=source_row_i,
            target_col_i=target_col_i,
            target_row_i=target_row_i,
            board=board.copy_board(),
        )
        return Move(
            player_sign=player_sign,
            result_board=result_board,
            result_ball_position=cls.push_ball(
                player_sign=player_sign,
                ball_position=board.ball_position,
            ),
            description=description,
            used_card_index=card_index,
        )

    @classmethod
    def push_ball(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> BallPosition:
        match player_sign, ball_position:
            case PlayerSign.white, BallPosition.middle:
                return BallPosition.black
            case PlayerSign.white, BallPosition.white:
                return BallPosition.middle
            case PlayerSign.black, BallPosition.middle:
                return BallPosition.white
            case PlayerSign.black, BallPosition.black:
                return BallPosition.middle
        raise RuntimeError(f"Cannot push ball. Player: {player_sign}, ball position: {ball_position}")
