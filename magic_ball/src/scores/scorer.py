from board_utils import BoardUtils
from models import PlayerSign, BoardType, BallPosition
from players.player_config import PlayerConfig


class Scorer:
    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        assert config.score_multipliers is not None
        self._player_sign = player_sign
        self._config = config

    def score_move(
        self,
        board: BoardType,
        ball_position: BallPosition,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> int:
        """
        Maximal score is best.
        Method: score board for each player and reduce the player score from the opponent score.
        This means: positive score means player has the advantage and negative score means the opponent has advantage.
        """
        # Always choose a winning move.
        if BoardUtils.is_player_win(
            player_sign=self._player_sign,
            board=board,
        ):
            return 99999999999
        # Always avoid a losing move.
        if BoardUtils.is_player_one_to_win(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=self._player_sign,
            ),
            board=board,
        ):
            return -99999999999

        return self._score_move_for_player(
            player_sign=self._player_sign,
            board=board,
            ball_position=ball_position,
            num_unused_player_cards=num_unused_player_cards,
            num_unused_opponent_cards=num_unused_opponent_cards,
        ) - self._score_move_for_player(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=self._player_sign,
            ),
            board=board,
            ball_position=ball_position,
            num_unused_player_cards=num_unused_opponent_cards,
            num_unused_opponent_cards=num_unused_player_cards,
        )

    def _score_move_for_player(
        self,
        player_sign: PlayerSign,
        board: BoardType,
        ball_position: BallPosition,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> int:
        multipliers = self._config.score_multipliers
        ball_position_score = self._ball_score(
            player_sign=player_sign,
            ball_position=ball_position,
        )

        # TODO: board score

        return (
            multipliers.num_unused_player_cards_score * num_unused_player_cards
            - multipliers.num_unused_player_cards_score * num_unused_opponent_cards
            + ball_position_score
        )

    def _ball_score(
        self,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> int:
        return (
            0
            if ball_position == BallPosition.middle
            else 1
            if self._is_ball_at_player(
                player_sign=player_sign,
                ball_position=ball_position,
            )
            else -1
        ) * self._config.score_multipliers.ball_position_score

    @classmethod
    def _is_ball_at_player(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> bool:
        return (
            (ball_position == BallPosition.white and player_sign == PlayerSign.white)
            or (ball_position == BallPosition.black and player_sign == PlayerSign.black)
        )
