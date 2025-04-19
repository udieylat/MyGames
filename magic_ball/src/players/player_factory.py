from models import PlayerSign
from players.human_player import HumanPlayer
from players.player_config import PlayerConfig, PlayerType
from players.random_player import RandomPlayer


class PlayerFactory:
    @classmethod
    def generate_player(
        cls,
        player_config: PlayerConfig,
        player_sign: PlayerSign,
    ) -> HumanPlayer | RandomPlayer | None:
        match player_config.type:
            case PlayerType.human:
                return HumanPlayer(
                    player_sign=player_sign,
                )
            case PlayerType.random:
                return RandomPlayer(
                    player_sign=player_sign,
                )
            case PlayerType.base_heuristic:
                return BaseHeuristicPlayer(
                    player_sign=player_sign,
                )
        assert f"Invalid player type: {player_config.type}"
