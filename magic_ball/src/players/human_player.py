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
    ) -> Move:
        raise NotImplemented("find your own move")
