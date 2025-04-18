from magic_ball.src.board import Board
from magic_ball.src.models import PlayerType


class GameManager:

    def __init__(
        self,
        white_player: PlayerType = PlayerType.human,  # TODO: change to Player with strategy, etc
        black_player: PlayerType = PlayerType.human,
    ):
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._player_turn: PlayerType = self._white_player

        self._board.display()

    def play(
        self,
        move: Move,
    ):
        pass
