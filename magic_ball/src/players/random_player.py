import random

from board import Board
from cards.card import Card
from helper import Helper
from move import Move
from players.player import Player, NoAvailableMoves


class RandomPlayer(Player):

    def find_move(
        self,
        board: Board,
        player_cards: list[Card],
        opponent_cards: list[Card],
    ) -> Move:
        num_allowed_playable_cards = min(len(player_cards), len(opponent_cards))
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
            cards=self._cards,
            num_allowed_playable_cards=num_allowed_playable_cards,
        )
        if not available_moves:
            raise NoAvailableMoves()

        return random.choice(available_moves)
