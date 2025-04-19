from abc import abstractmethod

from board import Board
from move import PossibleMoveType
from models import PlayerSign


class Player:

    def __init__(
        self,
        player_sign: PlayerSign,
        # magic_cards: list[MagicCard]
    ):
        self._player_sign = player_sign

    @property
    def player_sign(self) -> PlayerSign:
        return self._player_sign

    @property
    def is_human(self) -> bool:
        return False

    @abstractmethod
    def find_move(
        self,
        board: Board,
    ) -> PossibleMoveType:
        pass
