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
    #     self._cards: list[CardType] = []
    #
    # def draw_cards(self, cards: list[CardType]):
    #     self._cards = cards

    @property
    def player_sign(self) -> PlayerSign:
        return self._player_sign

    @property
    def is_human(self) -> bool:
        return False

    def get_card_available_moves(
        self,
        card_index: int,
    ) -> list[Move]:
        # TODO: verify that index is not used
        pass

    @abstractmethod
    def find_move(
        self,
        board: Board,
    ) -> Move:
        pass
