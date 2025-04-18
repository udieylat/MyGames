from dataclasses import dataclass

from magic_ball.src.models import PlayerType


@dataclass
class Player:
    player_type: PlayerType

    # TODO: strategy
