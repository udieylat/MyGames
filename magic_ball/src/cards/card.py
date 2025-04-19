from abc import abstractmethod

from board import Board
from models import PlayerSign
from move import Move


class Card:
    def __init__(self):
        self._already_used = False

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def is_defensive(self) -> bool:
        return False

    def use_card(self):
        assert not self._already_used
        self._already_used = True

    @abstractmethod
    def get_available_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        if self._already_used:
            return []
        return self._get_available_moves(
            player_sign=player_sign,
            board=board,
            card_index=card_index,
        )

    @abstractmethod
    def _get_available_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pass
