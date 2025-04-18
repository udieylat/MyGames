from magic_ball.src.board import Board, InvalidMove
from magic_ball.src.models import PlayerSign
from magic_ball.src.player import Player


class GameManager:

    def __init__(
        self,
        white_player: Player,
        black_player: Player,
    ):
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._player_turn: PlayerSign = PlayerSign.white

        self._board.display()

    def push(
        self,
        target_tile: str,
    ):
        try:
            self._board.push(
                target_tile=target_tile,
                player=self._player_turn,
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
            PlayerSign.white
            if self._player_turn == PlayerSign.black
            else PlayerSign.black
        )
        # TODO: check win condition
        # TODO: what more?
