from abc import abstractmethod

from board import Board
from move import Move
from models import PlayerSign


class Player:

    def __init__(
        self,
        player_sign: PlayerSign,
    ):
        self._player_sign = player_sign
    #     self._cards: set[CardType] = set()
    #
    # def draw_cards(self, cards: set[CardType]):
    #     self._cards = cards

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
    ) -> Move:
        pass
