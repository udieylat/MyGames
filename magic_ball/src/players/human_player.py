from board import Board
from cards.card import Card
from move import Move
from players.player import Player


class HumanPlayer(Player):

    @property
    def is_human(self) -> bool:
        return True

    def find_move(
        self,
        board: Board,
        unused_player_cards: list[Card],
        unused_opponent_cards: list[Card],
    ) -> Move:
        raise NotImplemented("find your own move")
