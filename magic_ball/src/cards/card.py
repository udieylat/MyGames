from abc import abstractmethod

from board import Board
from models import PlayerSign, BallPosition
from move import Move


class Card:
    def __init__(self):
        self._already_used = False

    @property
    def is_defensive(self) -> bool:
        return False

    def use_card(self):
        assert not self._already_used
        self._already_used = True

    def get_available_moves(
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
        return self._get_available_moves(
            player_sign=player_sign,
            board=board,
            card_index=card_index,
        )

    @classmethod
    def _ball_position_allowed(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> bool:
        # TODO: for "pull" card, override this function
        match player_sign, ball_position:
            case (PlayerSign.white, BallPosition.black) | (PlayerSign.black, BallPosition.white):
                return False
            case _:
                return True

    @classmethod
    @abstractmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pass
