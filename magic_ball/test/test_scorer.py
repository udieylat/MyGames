import unittest

from board import Board
from constants import DEFAULT_NUM_CARDS_PER_PLAYER
from helper import Helper
from models import PlayerSign, BallPosition
from players.player_config import PlayerConfig
from scores.scorer import Scorer


class TestScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = Scorer(
            player_sign=PlayerSign.white,
            config=PlayerConfig.default_ai_opponent(
                random_tie_break=False,
            ),
        )

    def test_score_new_board(self):
        score = self.scorer.score_board(
            board=Board.new().copy_board(),
            ball_position=BallPosition.middle,
            num_unused_player_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
            num_unused_opponent_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
        )
        self.assertEqual(0, score)

    def test_is_free_pawn(self):
        board = [
            ["W", "#", ".", "W", "."],
            [".", ".", "B", ".", "B"],
            [".", ".", "W", ".", "."],
            [".", ".", ".", ".", "B"],
            [".", "B", ".", "B", "B"],
        ]
        white_pawn_indices = Helper.get_pawn_indices(
            player_sign=PlayerSign.white,
            board=board,
        )
        black_pawn_indices = Helper.get_pawn_indices(
            player_sign=PlayerSign.black,
            board=board,
        )
        free_white_pawns_indices = [
            # TODO
        ]
        free_black_pawns_indices = [
            # TODO
        ]
        expected_free_white_pawns_indices = {
            (0, 0),
            (2, 2),
        }
        expected_free_black_pawns_indices = {
            (1, 2),
            (1, 4),
        }
        self.assertSetEqual(free_white_pawns_indices, expected_free_white_pawns_indices)
        self.assertSetEqual(free_black_pawns_indices, expected_free_black_pawns_indices)
