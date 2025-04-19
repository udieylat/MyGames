from abc import abstractmethod

from board import Board
from models import PlayerSign, BallPosition
from move import Move


class Card:
    def __init__(self):
        self._already_used = False

    # @property
    # @abstractmethod
    # def name(self) -> str:
    #     pass

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
    def _push_ball(
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

    @classmethod
    @abstractmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pass
