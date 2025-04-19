import random

from board import Board
from helper import Helper
from move import Move
from players.player import Player, NoAvailableMoves


class RandomPlayer(Player):

    def find_move(
        self,
        board: Board,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> Move:
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
            cards=self._cards,
        )
        if not available_moves:
            raise NoAvailableMoves()

        return random.choice(available_moves)
