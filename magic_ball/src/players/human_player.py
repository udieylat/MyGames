from board import Board
from move import PossibleMoveType
from players.player import Player


class HumanPlayer(Player):

    @property
    def is_human(self) -> bool:
        return True

    def find_move(
        self,
        board: Board,
    ) -> PossibleMoveType:
        raise NotImplemented("find your own move")
