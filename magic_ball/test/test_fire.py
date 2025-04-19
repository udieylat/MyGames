import unittest

from parameterized import parameterized

from board import Board
from board_utils import BoardUtils
from cards.fire import Fire
from models import PlayerSign, BallPosition


class TestFire(unittest.TestCase):
    def setUp(self):
        self.fire = Fire()
        self.board = Board.new()

    @parameterized.expand(PlayerSign.__members__.keys())
    def test_available_card_moves(self, player_sign: PlayerSign):
        available_moves = self.fire.get_available_card_moves(
            player_sign=player_sign,
            board=self.board,
            card_index=0,
        )
        self.assertEqual(1, len(available_moves))
        self.assertTrue(
            all(
                not BoardUtils.is_tile_player_pawn(
                    player_sign=player_sign,
                    tile=move.result_board[row_i][col_i],
                )
                for move in available_moves
                for row_i in range(5)
                for col_i in range(5)
            )
        )
