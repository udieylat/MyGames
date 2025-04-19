from dataclasses import dataclass
from typing import Union

from magic_ball.src.models import MoveType, PlayerSign


@dataclass
class Move:
    type: MoveType
    player_sign: PlayerSign


class PushMove(Move):
    type: MoveType = MoveType.push
    target_tile: str


class MagicCardMove(Move):
    type: MoveType = MoveType.magic_card
    # TODO


PossibleMoveType = Union[PushMove, MagicCardMove]
