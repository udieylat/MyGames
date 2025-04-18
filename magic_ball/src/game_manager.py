from magic_ball.src.board import Board, InvalidMove
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

    def push(
        self,
        target_tile: str,
    ):
        try:
            self._board.push(
                target_tile=target_tile,
                player=self._player_turn,  # TODO
            )
            self._complete_turn()
        except InvalidMove as e:
            print(f"** Invalid move: {e.description}")
            # self._board.display()

    def play_magic_card(
        self,
        move: str,
    ):
        # TODO
        pass

    def _complete_turn(self):
        self._player_turn = (
            self._white_player
            if self._player_turn == self._black_player
            else self._black_player
        )
        # TODO: check win condition
        # TODO: what more?
