import unittest

from parameterized import parameterized

from board import Board
from cards.knight import Knight
from models import PlayerSign, BallPosition, TileType


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

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_num_available_card_moves_center_tile(self, player_sign: PlayerSign):
        tile = (
            TileType.white
            if player_sign == PlayerSign.white
            else TileType.black
        )
        board = Board(
            board=[
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", tile, ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
            ],
            ball_position=BallPosition.middle,
        )
        available_moves = self.knight.get_available_card_moves(
            player_sign=player_sign,
            board=board,
            card_index=0,
        )
        self.assertEqual(6, len(available_moves))
