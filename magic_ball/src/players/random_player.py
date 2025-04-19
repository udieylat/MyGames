import random

from board import Board
from helper import Helper
from move import PossibleMoveType
from players.player import Player


class RandomPlayer(Player):

    @property
    def is_human(self) -> bool:
        return False

    def find_move(
        self,
        board: Board,
    ) -> PossibleMoveType:
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
        )
        assert available_moves, "No move to play"
        return random.choice(available_moves)
