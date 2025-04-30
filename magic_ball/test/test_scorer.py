import unittest

from board import Board
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from models import PlayerSign, BallPosition
from players.player_config import PlayerConfig, PlayerType, ScoreMultipliers
from scores.scorer import Scorer


class TestScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = Scorer(
            player_sign=PlayerSign.white,
            config=PlayerConfig.default_ai_opponent(),
        )

    def test_score_new_board(self):
        score = self.scorer.score_move(
            board=Board.new().copy_board(),
            ball_position=BallPosition.middle,
            num_unused_player_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
            num_unused_opponent_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
        )
        self.assertEqual(0, score)
