import unittest

from parameterized import parameterized

from board import Board
from cards.tank import Tank
from models import PlayerSign, BallPosition


class TestTank(unittest.TestCase):
    def setUp(self):
        self.tank = Tank()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves_starting_board(self, player_sign: PlayerSign):
        available_moves = self.tank.get_available_card_moves(
            player_sign=player_sign,
            board=Board.new(),
            card_index=0,
        )
        self.assertEqual(0, len(available_moves))

    def test_no_winning_available_card_move(self):
        board = Board(
            board=[
                [".", "W", ".", "W", "#"],
                ["B", ".", ".", ".", "."],
                ["W", ".", "W", ".", "."],
                [".", ".", "W", ".", "."],
                [".", "B", ".", "B", "B"],
            ],
            ball_position=BallPosition.middle,
        )
        available_moves = self.tank.get_available_card_moves(
            player_sign=PlayerSign.white,
            board=board,
            card_index=0,
        )
        self.assertEqual(1, len(available_moves))  # Only C4->C3 (back push the white pawn)
