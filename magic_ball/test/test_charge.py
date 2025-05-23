import unittest

from parameterized import parameterized

from board import Board
from cards.charge import Charge
from models import PlayerSign, BallPosition


class TestCharge(unittest.TestCase):
    def setUp(self):
        self.charge = Charge()
        self.board = Board.new()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves(self, player_sign: PlayerSign):
        available_moves = self.charge.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(10, len(available_moves))
