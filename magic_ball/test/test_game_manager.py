import unittest

from game_manager import GameManager
from helper import Helper
from models import GameStatus
from players.player_config import PlayerConfig, PlayerType


class TestGameManager(unittest.TestCase):
    def test_base_push_game(self):
        gm = GameManager.new(
            cards_pull=[],
        )
        gm.push("D2")
        gm.push("D4")
        gm.push("D3")
        gm.push("A4")
        gm.push("A2")
        gm.push("A3")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)
        gm.push("B2")
        gm.push("B4")
        gm.push("B3")
        gm.push("E4")
        gm.push("E2")
        gm.push("E3")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)
        gm.push("C2")
        gm.push("C4")
        gm.push("C3")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.white_defensive_win)  # Defensive win since no cards

    def test_base_push_game_vs_random_ai_in_black(self):
        gm = GameManager.new(
            black_player_config=PlayerConfig(
                type=PlayerType.random,
            ),
            cards_pull=[],
        )
        gm.push("A2")
        gm.push("B2")
        gm.push("C2")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)

    def test_base_push_game_vs_random_ai_in_white(self):
        gm = GameManager.new(
            white_player_config=PlayerConfig(
                type=PlayerType.random,
            ),
            cards_pull=[],
        )
        gm.push("A4")
        gm.push("B4")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)

    def test_random_ai_base_push_game(self):
        gm = GameManager.new(
            white_player_config=PlayerConfig(
                type=PlayerType.random,
            ),
            black_player_config=PlayerConfig(
                type=PlayerType.random,
            ),
            cards_pull=[],
        )

        # No cards scenario means white defensive win.
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.white_defensive_win)

    @classmethod
    def _get_game_status(cls, gm: GameManager) -> GameStatus:
        return Helper.get_game_status(
            board=gm._board,
            white_cards=gm._white_player.cards,
            black_cards=gm._black_player.cards,
        )
