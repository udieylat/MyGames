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
        """
        Expected log:
         1. A2 ; A4
         2. B2 ; A3
         3. knight: B2->A4 ; knife pawn: A4
         4. C2 ; B4
         5. D2 ; B3
         6. wall: B2 ; C4
         7. E2 ; C3
         8. D3 ; D4
         9. E3 ; E4
         10. pass ; bishop: C3->D2
         11. kamikaze: eliminate pawns D2 (opponent) and C2 (player) ; sidestep: B3->C3
         12. pass ; C2
         13. pass ; C1

        Final board position:
            5 . . . . .
            4 . . . B B
            3 B . . W W
            2 W # . . .
            1 . . B . .
              A B C D E
        """
        filename = os.path.dirname(os.path.abspath(__file__))
        gm = GameManager.from_config_filename(f"{filename}/../config/fixed_game.json")
        # gm.log()
        game_summary = gm.export_summary()
        self.assertEqual(game_summary.winner, "black")
        self.assertEqual(game_summary.num_white_moves, 13)
        self.assertEqual(game_summary.final_ball_position, "middle")

    def test_fixed_position_fire_loses(self):
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
        gm = self._black_ai_turn_vs_human(
            board=board,
            black_card_names=["fire"],
        )

        # Assert "fire" was NOT played by black.
        self.assertFalse(
            all(
                board[row_i][col_i] == TileType.vacant
                for row_i in range(1, 4)
                for col_i in range(0, 5)
            ),
            msg=f"Unexpected 'fire' play, game log: {gm._game_log}",
        )

    def test_fixed_position_black_push_to_win(self):
        """
        Naive score would suggest "charge" improves black's position.
        But, black is "free push to win" (has ball position).
        """
        self.assertNotIn("pull", Compendium.get_cards_names(), msg="Logic is broken if 'pull' is in play")

        board = Board(
            board=[
                ["W", "W", ".", "W", "W"],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", "B", "B", "B", "B"],
            ],
            ball_position=BallPosition.black,
        )
        gm = self._black_ai_turn_vs_human(
            board=board,
            black_card_names=["charge"],
        )

        # Only one reasonable play here: C4.
        self.assertEqual("C4", gm._game_log[-1], msg=f"Unexpected play, game log: {gm._game_log}")
        self.assertEqual(board[3][2], TileType.black)
        self.assertEqual(board[4][2], TileType.vacant)
        self.assertEqual(board.ball_position, BallPosition.black)

    def test_fixed_position_black_must_sidestep(self):
        board = Board(
            board=[
                ['.', '.', '.', '.', '.'],
                ['.', '.', '.', '#', 'W'],
                ['W', '.', '.', '.', '.'],
                ['.', 'B', 'B', '.', 'W'],
                ['.', '.', '.', '.', 'B']
            ],
            ball_position=BallPosition.middle,
        )
        gm = self._black_ai_turn_vs_human_with_config(
            board=board,
            cards_config=CardsConfig(
                num_black_cards=1,
                num_white_cards=1,
                black_card_names=["sidestep"],
            ),
        )
        # Only one reasonable play here: sidestep: B4->A4.
        self.assertEqual("sidestep: B4->A4", gm._game_log[-1], msg=f"Unexpected play, game log: {gm._game_log}")
        self.assertEqual(board.ball_position, BallPosition.white)

    @classmethod
    def _get_game_status(cls, gm: GameManager) -> GameStatus:
        return Helper.get_game_status(
            board=gm._board,
            white_cards=gm._white_player.cards,
            black_cards=gm._black_player.cards,
        )

    @classmethod
    def _black_ai_turn_vs_human(
        cls,
        board: Board,
        black_card_names: list[str],
    ) -> GameManager:
        return cls._black_ai_turn_vs_human_with_config(
            board=board,
            cards_config=CardsConfig(
                black_card_names=black_card_names,
            ),
        )

    @classmethod
    def _black_ai_turn_vs_human_with_config(
        cls,
        board: Board,
        cards_config: CardsConfig,
    ) -> GameManager:
        return GameManager(
            config=GameConfig(
                black_player=PlayerConfig.default_ai_opponent(),
                cards_config=cards_config,
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
