from board import Board
from board_utils import BoardUtils
from helper import Helper
from models import PlayerSign
from move import Move
from players.player import Player
from players.player_config import PlayerConfig
from scores.scorer import Scorer


class BaseHeuristicPlayer(Player):
    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        super().__init__(
            player_sign=player_sign,
        )
        self._scorer = Scorer(
            player_sign=player_sign,
            config=config,
        )

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

        # Choose the first winning move if exists.
        # winning_move = next(
        #     (
        #         move
        #         for move in available_moves
        #         if BoardUtils.is_player_win(
        #             player_sign=self._player_sign,
        #             board=move.result_board,
        #         )
        #     ),
        #     None,
        # )
        # if winning_move is not None:
        #     return winning_move

        return available_moves[0]  # TODO!
