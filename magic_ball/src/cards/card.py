from abc import abstractmethod

from board import Board
from models import PlayerSign
from move import Move


class Card:
    def __init__(self):
        self._already_used = False

    @property
    def is_defensive(self) -> bool:
        return False

    @property
    def already_used(self) -> bool:
        return self._already_used

    def use_card(self):
        assert not self._already_used
        self._already_used = True

    @abstractmethod
    def get_available_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
    ) -> list[Move]:
        pass
