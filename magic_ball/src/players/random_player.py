import random

from board import Board
from helper import Helper
from move import Move
from players.player import Player


class RandomPlayer(Player):

    @property
    def is_human(self) -> bool:
        return False

    def find_move(
        self,
        board: Board,
    ) -> Move:
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
        )
        assert available_moves, "No move to play"
        return random.choice(available_moves)
