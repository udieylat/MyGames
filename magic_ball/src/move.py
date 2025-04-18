from dataclasses import dataclass

from magic_ball.src.models import MoveType


@dataclass
class Move:
    type: MoveType


class PushMove(Move):
    type: MoveType = MoveType.push
    target_tile: str


class MagicCardMove(Move):
    type: MoveType = MoveType.magic_card
    # TODO
