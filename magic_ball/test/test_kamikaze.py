import unittest

from parameterized import parameterized

from board import Board
from cards.kamikaze import Kamikaze
from models import PlayerSign


class TestKamikaze(unittest.TestCase):
    def setUp(self):
        self.kamikaze = Kamikaze()
        self.board = Board.new()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves(self, player_sign: PlayerSign):
        available_moves = self.kamikaze.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(7, len(available_moves))
