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
        self._board_example = [
            ["W", "#", ".", "W", "."],
            [".", ".", "B", ".", "B"],
            [".", ".", "W", ".", "."],
            [".", ".", ".", ".", "B"],
            [".", "B", ".", "B", "B"],
        ]

    def test_score_new_board(self):
        score = self.scorer.score_board(
            board=Board.new().copy_board(),
            ball_position=BallPosition.middle,
            num_used_player_cards=0,
            num_used_opponent_cards=0,
            num_allowed_playable_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
        )
        self.assertEqual(0, score)

    def test_is_free_pawn(self):
        white_pawn_indices = Helper.get_pawn_indices(
            player_sign=PlayerSign.white,
            board=self._board_example,
        )
        black_pawn_indices = Helper.get_pawn_indices(
            player_sign=PlayerSign.black,
            board=self._board_example,
        )
        free_white_pawns_indices = {
            (col_i, row_i)
            for col_i, row_i in white_pawn_indices
            if self.scorer._is_free_pawn(
                player_sign=PlayerSign.white,
                board=self._board_example,
                col_i=col_i,
                row_i=row_i,
            )
        }
        free_black_pawns_indices = {
            (col_i, row_i)
            for col_i, row_i in black_pawn_indices
            if self.scorer._is_free_pawn(
                player_sign=PlayerSign.black,
                board=self._board_example,
                col_i=col_i,
                row_i=row_i,
            )
        }
        expected_free_white_pawns_indices = {
            (0, 0),
            (2, 2),
        }
        expected_free_black_pawns_indices = {
            (2, 1),
            (4, 1),
        }
        self.assertSetEqual(free_white_pawns_indices, expected_free_white_pawns_indices)
        self.assertSetEqual(free_black_pawns_indices, expected_free_black_pawns_indices)

    def test_get_free_pawn_distances_from_start_tile(self):
        free_white_pawn_distances_from_start_tile = self.scorer._get_free_pawn_distances_from_start_tile(
            player_sign=PlayerSign.white,
            board=self._board_example,
        )
        free_black_pawn_distances_from_start_tile = self.scorer._get_free_pawn_distances_from_start_tile(
            player_sign=PlayerSign.black,
            board=self._board_example,
        )
        self.assertListEqual([0, 2], free_white_pawn_distances_from_start_tile)
        self.assertListEqual([3, 3], free_black_pawn_distances_from_start_tile)

    def test_winning_score(self):
        board = [
            ["W", "W", "W", "W", "W"],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "B", "B", "B", "B"],
        ]
        self.assertIsNotNone(
            self.scorer._winning_score(
                board=board,
                ball_position=BallPosition.white,
            )
        )
        self.assertIsNone(
            self.scorer._winning_score(
                board=board,
                ball_position=BallPosition.middle,
            )
        )

    def test_losing_score(self):
        board = [
            ["W", "W", "W", "W", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "B"],
            [".", "B", "B", "B", "."],
        ]
        self.assertIsNotNone(
            self.scorer._losing_score(
                board=board,
                ball_position=BallPosition.black,
            )
        )
        self.assertIsNone(
            self.scorer._losing_score(
                board=board,
                ball_position=BallPosition.middle,
            )
        )

    def test_num_moves_to_win(self):
        board = [
            ["W", "W", "W", "W", "W"],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "B", "B", "B", "B"],
        ]
        num_moves_to_win = self.scorer._num_moves_to_win(
            board=board,
            ball_position=BallPosition.white,
        )
        self.assertEqual(4, num_moves_to_win)

        board = [
            [".", "W", "W", "W", "W"],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            ["W", ".", ".", ".", "."],
            [".", "B", "B", "B", "B"],
        ]
        num_moves_to_win = self.scorer._num_moves_to_win(
            board=board,
            ball_position=BallPosition.white,
        )
        self.assertEqual(1, num_moves_to_win)

    def test_score_distant_free_pawn(self):
        board = [
            ["W", "W", "W", "W", "W"],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "B", "B", "B", "B"],
        ]
        score_distant_free_pawn = self.scorer.score_board(
            board=board,
            ball_position=BallPosition.white,
            num_used_player_cards=0,
            num_used_opponent_cards=0,
            num_allowed_playable_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
        )

        board = [
            [".", "W", "W", "W", "W"],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            ["W", ".", ".", ".", "."],
            [".", "B", "B", "B", "B"],
        ]
        score_close_free_pawn = self.scorer.score_board(
            board=board,
            ball_position=BallPosition.white,
            num_used_player_cards=0,
            num_used_opponent_cards=0,
            num_allowed_playable_cards=DEFAULT_NUM_CARDS_PER_PLAYER,
        )
        self.assertGreater(score_close_free_pawn, score_distant_free_pawn)
