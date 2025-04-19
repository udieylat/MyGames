import random

from board import Board
from helper import Helper
from move import Move
from players.player import Player


class BaseHeuristicPlayer(Player):

    def find_move(
        self,
        board: Board,
    ) -> Move:
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
            cards=self._cards,
        )
        assert available_moves, "No move to play"
        return available_moves[0]  # TODO!
