from dataclasses import dataclass

from magic_ball import Board
from magic_ball import PlayerType, PlayerSign
from magic_ball import Move


@dataclass
class Player:
    player_sign: PlayerSign
    player_type: PlayerType
    # magic_cards: list[MagicCard]

    def play(self):
        pass

    def get_available_moves(
        self,
        board: Board,
    ) -> list[Move]:
        # TODO
        pass

    # TODO: strategy
