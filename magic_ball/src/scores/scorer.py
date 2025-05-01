import random

from board_utils import BoardUtils
from helper import Helper
from models import PlayerSign, BoardType, BallPosition, TileType
from players.player_config import PlayerConfig


class Scorer:

    WINNING_SCORE = 99999999999
    LOSING_SCORE = -WINNING_SCORE

    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        assert config.score_multipliers is not None
        self._player_sign = player_sign
        self._config = config

    def score_board(
        self,
        board: BoardType,
        ball_position: BallPosition,
        num_unused_player_cards: int,
        num_unused_opponent_cards: int,
    ) -> float:
        """
        Maximal score is best.
        Method: score board for each player and reduce the opponent score from the player score.
        This means: positive score means player has the advantage and negative score means the opponent has advantage.
        """
        # Always choose a winning move.
        if self._is_winning_move(
            board=board,
            ball_position=ball_position,
        ):
            return self.WINNING_SCORE
        # Always avoid a losing move.
        if self._is_losing_move(
            board=board,
            ball_position=ball_position,
        ):
            return self.LOSING_SCORE

        board_score_for_player = self._score_board_for_player(
            player_sign=self._player_sign,
            board=board,
            ball_position=ball_position,
            num_unused_player_cards=num_unused_player_cards,
        )
        board_score_for_opponent = self._score_board_for_player(
            player_sign=BoardUtils.inverse_player_sign(
                player_sign=self._player_sign,
            ),
            board=board,
            ball_position=ball_position,
            num_unused_player_cards=num_unused_opponent_cards,
        )
        return board_score_for_player - board_score_for_opponent

    def _is_winning_move(
        self,
        board: BoardType,
        ball_position: BallPosition,
    ) -> bool:
        # Game won by player - the move is the final winning move.
        if BoardUtils.is_player_win(
            player_sign=self._player_sign,
            board=board,
        ):
            return True

        # Winning move if the result board gives the player a free push to win.
        if self._is_player_free_push_to_win(
            board=board,
            ball_position=ball_position,
        ):
            return True

        return False

    def _is_losing_move(
        self,
        board: BoardType,
        ball_position: BallPosition,
    ) -> bool:
        # Losing move if the result board gives the opponent a single push to win.
        if BoardUtils.is_player_single_push_to_win(
            player_sign=self._opponent_player_sign,
            board=board,
        ):
            return True

        # Losing move if the result board gives the opponent a free push to win.
        if self._is_opponent_free_push_to_win(
            board=board,
            ball_position=ball_position,
        ):
            return True

        return False

    def _is_player_free_push_to_win(
        self,
        board: BoardType,
        ball_position: BallPosition,
    ) -> bool:
        """
        If the ball position is at the player, and they have a free pawn then the opponent cannot stop their free pawn.
        Therefore, if their free pawn distance is farther than the opponent's farthest free pawn,
        the player is "free push to win" and the board is winning for the player.

        Notice: this doesn't work if "pull" card is in play.
        """
        pass

    def _is_opponent_free_push_to_win(
        self,
        board: BoardType,
        ball_position: BallPosition,
    ) -> bool:
        """
        If the ball position is at the opponent, and they have a free pawn then the player cannot stop their free pawn.
        Therefore, if their free pawn distance is farther or equal to the player's farthest free pawn,
        the opponent is "free push to win" and the board is losing for the player.

        Notice: this doesn't work if "pull" card is in play.
        """
        if not self._is_ball_at_player(
            player_sign=self._opponent_player_sign,
            ball_position=ball_position,
        ):
            return False

        free_opponent_pawn_distances_from_start_tile = self._get_free_pawn_distances_from_start_tile(
            player_sign=self._opponent_player_sign,
            board=board,
            pawn_indices=Helper.get_pawn_indices(
                player_sign=self._opponent_player_sign,
                board=board,
            ),
        )
        if not free_opponent_pawn_distances_from_start_tile:
            return False

        free_player_pawn_distances_from_start_tile = self._get_free_pawn_distances_from_start_tile(
            player_sign=self._player_sign,
            board=board,
            pawn_indices=Helper.get_pawn_indices(
                player_sign=self._player_sign,
                board=board,
            ),
        )
        if not free_player_pawn_distances_from_start_tile:
            return True

        farthest_free_opponent_pawn_distance = max(free_opponent_pawn_distances_from_start_tile)
        farthest_free_player_pawn_distance = max(free_player_pawn_distances_from_start_tile)
        return farthest_free_opponent_pawn_distance >= farthest_free_player_pawn_distance

    def _score_board_for_player(
        self,
        player_sign: PlayerSign,
        board: BoardType,
        ball_position: BallPosition,
        num_unused_player_cards: int,
    ) -> float:

        # TODO: no opponent unused cards is a huge advantage (only against a human player)

        return (
            self._config.score_multipliers.score_per_unused_card * num_unused_player_cards
            + self._board_score(
                player_sign=player_sign,
                board=board,
            )
            + self._ball_score(
                player_sign=player_sign,
                ball_position=ball_position,
            )
            + self._random_tie_break_if_necessary()
        )

    def _board_score(
        self,
        player_sign: PlayerSign,
        board: BoardType,
    ) -> int:
        pawn_indices = Helper.get_pawn_indices(
            player_sign=player_sign,
            board=board,
        )
        free_pawn_distances_from_start_tile = self._get_free_pawn_distances_from_start_tile(
            player_sign=player_sign,
            board=board,
            pawn_indices=pawn_indices,
        )

        num_pawns_score = len(pawn_indices) * self._config.score_multipliers.score_per_pawn
        free_pawns_score = len(free_pawn_distances_from_start_tile) * self._config.score_multipliers.score_per_free_pawn
        free_pawns_distance_score = sum(
            free_pawn_distance_from_start_tile * self._config.score_multipliers.free_pawn_score_per_distance_from_start_tile
            for free_pawn_distance_from_start_tile in free_pawn_distances_from_start_tile
        )
        return num_pawns_score + free_pawns_score + free_pawns_distance_score

    @classmethod
    def _get_free_pawn_distances_from_start_tile(
        cls,
        player_sign: PlayerSign,
        board: BoardType,
        pawn_indices: list[tuple[int, int]],
    ) -> list[int]:
        """
        Return list of "free pawns" distances from start tile for input player.
        Every distance value represents a free pawn and how many tiles it's from the starting tile.
        Example:
            - player (white or black) has 2 free pawns, one at the starting row and one at row 3 (middle row).
            - Return value: [0, 2]
        """
        free_pawn_row_indices = [
            row_i
            for col_i, row_i in pawn_indices
            if cls._is_free_pawn(
                player_sign=player_sign,
                board=board,
                col_i=col_i,
                row_i=row_i,
            )
        ]
        return (
            free_pawn_row_indices
            if player_sign == PlayerSign.white
            else [
                4 - free_pawn_row_index
                for free_pawn_row_index in free_pawn_row_indices
            ]
        )

    @classmethod
    def _is_free_pawn(
        cls,
        player_sign: PlayerSign,
        board: BoardType,
        col_i: int,
        row_i: int,
    ) -> bool:
        rows_range = (
            range(row_i + 1, 5)
            if player_sign == PlayerSign.white
            else range(row_i - 1, -1, -1)
        )
        return all(
            board[target_row_i][col_i] == TileType.vacant
            for target_row_i in rows_range
        )

    def _ball_score(
        self,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> int:
        return (
            self._config.score_multipliers.ball_position_score
            if self._is_ball_at_player(
                player_sign=player_sign,
                ball_position=ball_position,
            )
            else 0
        )

    @property
    def _opponent_player_sign(self) -> PlayerSign:
        return BoardUtils.inverse_player_sign(
            player_sign=self._player_sign,
        )

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

    def _random_tie_break_if_necessary(self) -> float:
        return (
            random.random()
            if self._config.random_tie_break
            else 0.0
        )
