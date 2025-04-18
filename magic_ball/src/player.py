from dataclasses import dataclass

from magic_ball.src.models import PlayerSign, PlayerType


@dataclass
class Player:
    player_sign: PlayerSign
    player_type: PlayerType
