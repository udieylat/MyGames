from __future__ import annotations

from board import InvalidMove, Board
from helper import Helper
from players.player import Player
from models import PlayerSign, PlayerType, GameStatus
from move import PushMove


class GameManager:

    @classmethod
    def new(
        cls,
        white_type: PlayerType = PlayerType.human,
        black_type: PlayerType = PlayerType.human,
    ) -> GameManager:
        return GameManager(
            white_player=Player(
                player_sign=PlayerSign.white,
                player_type=white_type,
            ),
            black_player=Player(
                player_sign=PlayerSign.black,
                player_type=black_type,
            ),
        )

    def __init__(
        self,
        white_player: Player,
        black_player: Player,
    ):
        self._white_player = white_player
        self._black_player = black_player
        self._board = Board()

        self._player_turn: PlayerSign = PlayerSign.white

        self._game_on = True
        self._play_ai_player_turn_if_necessary()
        self._display()

    def __repr__(self) -> str:
        self._display()
        return ""

    def push(
        self,
        target_tile: str,
    ):
        if not self._game_on:
            print("Game is already over.")
            return
        try:
            self._board.play_move(
                move=PushMove(
                    player_sign=self._player_turn,
                    target_tile=target_tile,
                ),
            )
            self._complete_turn()
        except InvalidMove as e:
            print(f"** Invalid move: {e.description}")
            self._display()

    def play_magic_card(
        self,
        # TODO arg
    ):
        if not self._game_on:
            print("Game is already over.")
            return

        # TODO
        pass

    def pass_turn(self):
        if not self._game_on:
            print("Game is already over.")
            return

        available_moves = Helper.get_available_moves(
            player_sign=self._player_turn,
            board=self._board,
        )
        if available_moves:
            print("Cannot pass turn, there are available moves.")
        else:
            print("Pass turn, no available moves for player.")
            self._complete_turn()

    def _display(self):
        self._board.display()
        print(f"Player turn: {self._player_turn}")

    def _complete_turn(self):
        self._player_turn = (
            PlayerSign.white
            if self._player_turn == PlayerSign.black
            else PlayerSign.black
        )
        self._check_end_condition()
        self._play_ai_player_turn_if_necessary()
        self._display()

    def _check_end_condition(self):
        game_status = Helper.get_game_status(
            board=self._board,
        )
        match game_status:
            case GameStatus.white_win:
                print("White wins!")
                self._game_on = False
            case GameStatus.black_win:
                print("Black wins!")
                self._game_on = False
            case GameStatus.draw:
                print("Game is drawn!")
                self._game_on = False

    def _play_ai_player_turn_if_necessary(self):
        if not self._game_on:
            return

        player = (
            self._white_player
            if self._player_turn == PlayerSign.white
            else self._black_player
        )
        if player.player_type == PlayerType.human:
            return

        move = player.find_move(
            board=self._board,
        )
        self._board.play_move(
            move=move,
        )
        self._complete_turn()
