import unittest

from parameterized import parameterized

from board import Board
from cards.charge import Charge
from models import PlayerSign


class TestCharge(unittest.TestCase):
    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_moves(self, player_sign: PlayerSign):
        charge = Charge()
        available_moves = charge.get_available_moves(
            player_sign=player_sign,
            board=Board(),
            card_index=0,
        )
        self.assertEqual(15, len(available_moves))
