from abc import abstractmethod

from board import Board
from cards.card import Card
from move import Move
from models import PlayerSign


class NoAvailableMoves(Exception):
    pass


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
    def card_names(self) -> list[str]:
        return sorted(
            card.name
            for card in self.cards
        )

    @property
    def is_human(self) -> bool:
        return False

    @property
    def is_defensive(self) -> bool:
        return all(
            card.is_defensive
            for card in self.cards
        )

    @abstractmethod
    def find_move(
        self,
        board: Board,
        unused_player_cards: list[Card],
        unused_opponent_cards: list[Card],
    ) -> Move:
        pass
