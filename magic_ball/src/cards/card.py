from abc import abstractmethod

from board import Board
from board_utils import BoardUtils
from models import PlayerSign, BallPosition
from move import Move, CardMove


class Card:
    def __init__(self):
        self._already_used = False

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def description(cls) -> str:
        pass

    @property
    def already_used(self) -> bool:
        return self._already_used

    @property
    def is_defensive(self) -> bool:
        return False

    def use_card(self):
        assert not self._already_used
        self._already_used = True

    def get_available_card_moves(
        self,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[CardMove]:
        if self._already_used or not self._ball_position_allowed(
            player_sign=player_sign,
            ball_position=board.ball_position,
        ):
            return []
        available_moves = self._get_available_moves(
            player_sign=player_sign,
            board=board,
            card_index=card_index,
        )
        available_moves = self._filter_duplicate_description_moves(
            moves=available_moves,
        )
        return [
            move
            for move in available_moves
            if not BoardUtils.is_any_player_win(
                board=move.result_board,
            )
        ]

    @classmethod
    @abstractmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[CardMove]:
        pass

    @classmethod
    def _filter_duplicate_description_moves(
        cls,
        moves: list[CardMove],
    ) -> list[CardMove]:
        move_descriptions = set()
        non_duplicate_description_moves = []
        for move in moves:
            if move.description in move_descriptions:
                continue
            move_descriptions.add(move.description)
            non_duplicate_description_moves.append(move)
        return non_duplicate_description_moves

    @classmethod
    def _ball_position_allowed(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> bool:
        match player_sign, ball_position:
            case (PlayerSign.white, BallPosition.black) | (PlayerSign.black, BallPosition.white):
                return False
            case _:
                return True

    @classmethod
    def _describe_pawn_move(
        cls,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
    ) -> str:
        return BoardUtils.describe_pawn_move(
            card_name=str(cls.name),
            source_col_i=source_col_i,
            source_row_i=source_row_i,
            target_col_i=target_col_i,
            target_row_i=target_row_i,
        )
