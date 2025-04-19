import unittest

from parameterized import parameterized

from board import Board
from cards.pull import Pull
from models import PlayerSign, BallPosition


class TestPull(unittest.TestCase):
    def setUp(self):
        self.pull = Pull()
        self.board = Board()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_moves(self, player_sign: PlayerSign):
        available_moves = self.pull.get_available_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(1, len(available_moves))

    def test_no_available_moves(self):
        self.board._ball_position = BallPosition.white
        available_moves = self.pull.get_available_moves(
            player_sign=PlayerSign.white,
            board=self.board,
            card_index=0,
        )
        self.assertEqual([], available_moves)

        self.board._ball_position = BallPosition.black
        available_moves = self.pull.get_available_moves(
            player_sign=PlayerSign.black,
            board=self.board,
            card_index=0,
        )
        self.assertEqual([], available_moves)


    @parameterized.expand(PlayerSign.__members__.keys())
    def test_ball_position(self, player_sign: PlayerSign):
        available_moves = self.pull.get_available_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        expected_ball_position = (
            BallPosition.white
            if player_sign == PlayerSign.white
            else BallPosition.black
        )
        for move in available_moves:
            self.assertEqual(move.result_ball_position, expected_ball_position)
