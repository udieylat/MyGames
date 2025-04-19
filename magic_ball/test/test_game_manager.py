import unittest

from game_manager import GameManager
from models import GameStatus


class TestGameManager(unittest.TestCase):
    def test_base_push_game(self):
        gm = GameManager.new()
        gm.push("D2")
        gm.push("D4")
        gm.push("D3")
        gm.push("A4")
        gm.push("A2")
        gm.push("A3")
        self.assertEqual(gm._board.get_game_status(), GameStatus.ongoing)
        gm.push("B2")
        gm.push("B4")
        gm.push("B3")
        gm.push("E4")
        gm.push("E2")
        gm.push("E3")
        self.assertEqual(gm._board.get_game_status(), GameStatus.ongoing)
        gm.push("C2")
        gm.push("C4")
        gm.push("C3")
        self.assertEqual(gm._board.get_game_status(), GameStatus.draw)
