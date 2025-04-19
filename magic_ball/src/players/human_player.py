from board import Board
from move import Move
from players.player import Player


class HumanPlayer(Player):

    @property
    def is_human(self) -> bool:
        return True

    def find_move(
        self,
        board: Board,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> Move:
        raise NotImplemented("find your own move")
