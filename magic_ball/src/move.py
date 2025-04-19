from dataclasses import dataclass

from models import PlayerSign, MoveType


@dataclass
class PushMove:
    player_sign: PlayerSign
    target_tile: str
    type: MoveType = MoveType.push

    @property
    def description(self) -> str:
        return f"Push to target tile: {self.target_tile}"

@dataclass
class MagicCardMove:
    player_sign: PlayerSign
    # TODO
    type: MoveType = MoveType.magic_card

    @property
    def description(self) -> str:
        return ""


PossibleMoveType = PushMove | MagicCardMove
