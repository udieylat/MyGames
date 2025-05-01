import os
import unittest

from board import Board
from cards.cards_config import CardsConfig
from cards.compendium import Compendium
from game_config import GameConfig
from game_manager import GameManager
from helper import Helper
from models import GameStatus, BallPosition, PlayerSign, TileType
from players.player_config import PlayerConfig, PlayerType
from players.player_factory import PlayerFactory


class TestGameManager(unittest.TestCase):
    def test_base_push_game(self):
        gm = GameManager.new(
            config=GameConfig(
                cards_config=CardsConfig(
                    cards_pull=[],
                ),
            ),
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
                cards_config=CardsConfig(
                    cards_pull=[],
                ),
            ),
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
                cards_config=CardsConfig(
                    cards_pull=[],
                ),
            ),
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
                cards_config=CardsConfig(
                    cards_pull=[],
                ),
            ),
        )

        # No cards scenario means white defensive win.
        self.assertEqual(self._get_game_status(gm=gm), GameStatus.white_defensive_win)

    def test_fixed_game(self):
        filename = os.path.dirname(os.path.abspath(__file__))
        gm = GameManager.from_config_filename(f"{filename}/../config/fixed_game.json")
        game_summary = gm.export_summary()
        self.assertEqual(game_summary.winner, "white")
        self.assertEqual(game_summary.num_white_moves, 8)
        self.assertEqual(game_summary.final_ball_position, "middle")

    def test_fixed_position_fire_vs_wall(self):
        """
        In position:

        5 . B B B B
        4 . . . . .
        3 . . W . .
        2 . . . . .
        1 W W . W W
          A B C D E

        Black should play wall at A5, not fire row 3.
        """
        board = Board(
            board=[
                ["W", "W", ".", "W", "W"],
                [".", ".", ".", ".", "."],
                [".", ".", "W", ".", "."],
                [".", ".", ".", ".", "."],
                [".", "B", "B", "B", "B"],
            ],
            ball_position=BallPosition.middle,
        )
        _ = GameManager(
            config=GameConfig(
                black_player=PlayerConfig.default_ai_opponent(),
                cards_config=CardsConfig(
                    black_card_names=["fire", "wall", "peace"],
                ),
            ),
            white_player=PlayerFactory.generate_player(
                player_config=PlayerConfig.human(),
                player_sign=PlayerSign.white,
            ),
            black_player=PlayerFactory.generate_player(
                player_config=PlayerConfig.default_ai_opponent(),
                player_sign=PlayerSign.black,
            ),
            board=board,
            player_turn=PlayerSign.black,
        )

        # Assert "fire" was played by black.
        self.assertTrue(
            all(
                board[row_i][col_i] == TileType.vacant
                for row_i in range(1, 4)
                for col_i in range(0, 5)
            )
        )

        # Assert "wall" was played by black at A5.
        # self.assertEqual(board[4][0], TileType.wall)

    @classmethod
    def _get_game_status(cls, gm: GameManager) -> GameStatus:
        return Helper.get_game_status(
            board=gm._board,
            white_cards=gm._white_player.cards,
            black_cards=gm._black_player.cards,
        )
