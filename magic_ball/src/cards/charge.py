from board import Board
from cards.card import Card
from models import PlayerSign
from move import Move


class Charge(Card):
    def _get_available_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        pass
