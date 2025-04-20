from board import Board
from board_utils import BoardUtils
from cards.card import Card
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
        unused_player_cards: list[Card],
        unused_opponent_cards: list[Card],
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
                    num_unused_player_cards=len(unused_player_cards),
                    num_unused_opponent_cards=len(unused_opponent_cards),
                ),
                move,
            )
            for move in available_moves
        ]
        return max(scores_and_moves)[1]
