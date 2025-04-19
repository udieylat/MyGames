from dataclasses import dataclass
from typing import Union

from magic_ball import MoveType, PlayerSign


@dataclass
class PushMove:
    player_sign: PlayerSign
    target_tile: str
    type: MoveType = MoveType.push


@dataclass
class MagicCardMove:
    player_sign: PlayerSign
    # TODO
    type: MoveType = MoveType.magic_card


PossibleMoveType = Union[PushMove, MagicCardMove]
