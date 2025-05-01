import unittest

from parameterized import parameterized

from board import Board
from cards.tank import Tank
from models import PlayerSign


class TestTank(unittest.TestCase):
    def setUp(self):
        self.tank = Tank()
        self.board = Board.new()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves(self, player_sign: PlayerSign):
        available_moves = self.tank.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(0, len(available_moves))

