import os
import unittest

from game_manager import GameManager, GameConfig
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
            config=GameConfig(
                black_player=PlayerConfig(
                    type=PlayerType.random,
                ),
            ),
            cards_pull=[],
        )
        gm.push("A2")
        gm.push("B2")
        gm.push("C2")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)

    def test_base_push_game_vs_random_ai_in_white(self):
        gm = GameManager.new(
            config=GameConfig(
                white_player=PlayerConfig(
                    type=PlayerType.random,
                ),
            ),
            cards_pull=[],
        )
        gm.push("A4")
        gm.push("B4")
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.ongoing)

    def test_random_ai_base_push_game(self):
        gm = GameManager.new(
            config=GameConfig(
                white_player=PlayerConfig(
                    type=PlayerType.random,
                ),
                black_player=PlayerConfig(
                    type=PlayerType.random,
                ),
            ),
            cards_pull=[],
        )

        # No cards scenario means white defensive win.
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.white_defensive_win)

    def test_fixed_game(self):
        filename = os.path.dirname(os.path.abspath(__file__))
        gm = GameManager.from_config_filename(f"{filename}/../config/fixed_game.json")
        game_summary = gm.export_summary()
        self.assertEqual(game_summary.winner, "white")
        self.assertEqual(game_summary.num_white_moves, 7)
        self.assertEqual(game_summary.final_ball_position, "white")

    @classmethod
    def _get_game_status(cls, gm: GameManager) -> GameStatus:
        return Helper.get_game_status(
            board=gm._board,
            white_cards=gm._white_player.cards,
            black_cards=gm._black_player.cards,
        )
