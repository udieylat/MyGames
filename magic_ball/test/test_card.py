import itertools
import unittest

from parameterized import parameterized

from board import Board
from cards.card import Card
from cards.compendium import Compendium
from models import PlayerSign, BallPosition


class TestCard(unittest.TestCase):
    def setUp(self):
        self.board = Board.new()

    @parameterized.expand(
        itertools.product(
            PlayerSign.__members__.keys(),
            Compendium.get_cards(),
        )
    )
    def test_ball_position(self, player_sign: PlayerSign, card: Card):
        available_moves = card.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        expected_ball_position = (
            BallPosition.white
            if player_sign == PlayerSign.black
            else BallPosition.black
        )
        for move in available_moves:
            self.assertEqual(move.result_ball_position, expected_ball_position)
