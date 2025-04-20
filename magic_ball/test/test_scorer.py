import unittest

from board import Board
from models import PlayerSign, BallPosition
from players.player_config import PlayerConfig, PlayerType, ScoreMultipliers
from scores.scorer import Scorer


class TestScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = Scorer(
            player_sign=PlayerSign.white,
            config=PlayerConfig(
                type=PlayerType.base_heuristic,
                score_multipliers=ScoreMultipliers(
                    num_unused_player_cards_score=50,
                    ball_position_score=100,
                ),
            ),
        )

    def test_score_new_board(self):
        score = self.scorer.score_move(
            board=Board.new().copy_board(),
            ball_position=BallPosition.middle,
            num_unused_player_cards=3,
            num_unused_opponent_cards=3,
        )
        self.assertEqual(0, score)
