from board import Board
from board_utils import BoardUtils
from helper import Helper
from models import PlayerSign
from move import Move
from players.player import Player, NoAvailableMoves
from players.player_config import PlayerConfig
from scores.scorer import Scorer


class BaseHeuristicPlayer(Player):
    """
    Basically a next-move scorer player.
    """
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

        scores_and_moves = [
            (
                self._scorer.score_move(
                    result_board=move.result_board,
                    result_ball_position=move.result_ball_position,
                    num_unused_player_cards=0,
                    num_unused_opponent_cards=0,
                ),
                move,
            )
            for move in available_moves
        ]
        return min(scores_and_moves)[1]
