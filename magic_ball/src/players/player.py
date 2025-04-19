from abc import abstractmethod

from board import Board
from cards.card import Card
from move import Move
from models import PlayerSign


class Player:

    def __init__(
        self,
        player_sign: PlayerSign,
    ):
        self._player_sign = player_sign
        self._cards: list[Card] = []

    def draw_cards(self, cards: list[Card]):
        self._cards = cards

    @property
    def player_sign(self) -> PlayerSign:
        return self._player_sign

    @property
    def cards(self) -> list[Card]:
        return self._cards

    @property
    def is_human(self) -> bool:
        return False

    def get_available_card_moves(
        self,
        card_index: int,
        board: Board,
    ) -> list[Move]:
        assert 0 <= card_index <= 2, f"invalid card index: {card_index}"
        return self._cards[card_index].get_available_card_moves(
            player_sign=self._player_sign,
            board=board,
            card_index=card_index,
        )

    @abstractmethod
    def find_move(
        self,
        board: Board,
    ) -> Move:
        pass
