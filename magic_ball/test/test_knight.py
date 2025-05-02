import unittest

from parameterized import parameterized

from board import Board
from models import PlayerSign


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight = Knight()
        self.board = Board.new()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves(self, player_sign: PlayerSign):
        available_moves = self.knight.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(14, len(available_moves))
