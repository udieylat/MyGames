from board import Board
from helper import Helper
from models import PlayerSign
from move import Move
from players.player import Player
from players.player_config import PlayerConfig


class BaseHeuristicPlayer(Player):
    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        super().__init__(
            player_sign=player_sign,
        )
        self._config = config

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
