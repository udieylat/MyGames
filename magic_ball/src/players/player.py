from dataclasses import dataclass

from board import Board
from move import PossibleMoveType
from models import PlayerSign, PlayerType


@dataclass
class Player:
    player_sign: PlayerSign
    player_type: PlayerType
    # magic_cards: list[MagicCard]

    def play(self):
        pass

    # TODO: strategy
