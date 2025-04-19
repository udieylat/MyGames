from board_utils import BoardUtils
from models import PlayerSign, BoardType, BallPosition
from players.player_config import PlayerConfig


class Scorer:
    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        self._player_sign = player_sign
        self._config = config

    def score_move(
        self,
        result_board: BoardType,
        result_ball_position: BallPosition,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> int:
        """
        Minimal score is best.
        """
        # Always choose a winning move.
        if BoardUtils.is_player_win(
            player_sign=self._player_sign,
            board=result_board,
        ):
            return -99999999999
        # Always avoid a losing move.
        if BoardUtils.is_player_one_to_win(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=self._player_sign,
            ),
            board=result_board,
        ):
            return 99999999999
        # TODO
        return 0
