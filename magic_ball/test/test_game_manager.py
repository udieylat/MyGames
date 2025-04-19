import unittest

from game_manager import GameManager
from helper import Helper
from models import GameStatus, PlayerType


class TestGameManager(unittest.TestCase):
    def test_base_push_game(self):
        gm = GameManager.new()
        gm.push("D2")
        gm.push("D4")
        gm.push("D3")
        gm.push("A4")
        gm.push("A2")
        gm.push("A3")
        self.assertEqual(Helper.get_game_status(board=gm._board), GameStatus.ongoing)
        gm.push("B2")
        gm.push("B4")
        gm.push("B3")
        gm.push("E4")
        gm.push("E2")
        gm.push("E3")
        self.assertEqual(Helper.get_game_status(board=gm._board), GameStatus.ongoing)
        gm.push("C2")
        gm.push("C4")
        gm.push("C3")
        self.assertEqual(Helper.get_game_status(board=gm._board), GameStatus.draw)

    def test_base_push_game_vs_ai_in_black(self):
        gm = GameManager.new(
            black_type=PlayerType.ai,
        )
        gm.push("A2")
        gm.push("B2")
        gm.push("C2")
        self.assertEqual(Helper.get_game_status(board=gm._board), GameStatus.ongoing)

    def test_base_push_game_vs_ai_in_white(self):
        gm = GameManager.new(
            black_type=PlayerType.ai,
        )
        gm.push("A4")
        gm.push("B4")
        self.assertEqual(Helper.get_game_status(board=gm._board), GameStatus.ongoing)
