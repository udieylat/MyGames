from abc import abstractmethod

from board import Board
from board_utils import BoardUtils
from models import PlayerSign, BallPosition
from move import Move


class Card:
    def __init__(self):
        self._already_used = False

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__.lower()

    @property
    def already_used(self) -> bool:
        return self._already_used

    @property
    def is_defensive(self) -> bool:
        return False

    def use_card(self):
        assert not self._already_used
        self._already_used = True

    def get_available_card_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        if self._already_used or not self._ball_position_allowed(
            player_sign=player_sign,
            ball_position=board.ball_position,
        ):
            return []
        available_moves = self._get_available_moves(
            player_sign=player_sign,
            board=board,
            card_index=card_index,
        )
        for move in available_moves:
            assert not BoardUtils.is_any_player_win(
                board=move.result_board,
            ), f"Logical error, following card move is a winning move: {move.description}"
        return available_moves

    @classmethod
    @abstractmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pass

    @classmethod
    def _ball_position_allowed(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> bool:
        match player_sign, ball_position:
            case (PlayerSign.white, BallPosition.black) | (PlayerSign.black, BallPosition.white):
                return False
            case _:
                return True

    @classmethod
    def _describe_pawn_move(
        cls,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
    ) -> str:
        return BoardUtils.describe_pawn_move(
            card_name=str(cls.name),
            source_col_i=source_col_i,
            source_row_i=source_row_i,
            target_col_i=target_col_i,
            target_row_i=target_row_i,
        )
