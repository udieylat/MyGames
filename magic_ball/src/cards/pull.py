from board import Board
from cards.card import Card
from models import PlayerSign, BallPosition
from move import Move


class Pull(Card):
    """
    Shelved.
    Feels like it's anti-game, disabling the opponent from using all of their cards.
    Also, AI always starts with this play if available.
    """

    @property
    def is_defensive(self) -> bool:
        return True

    @classmethod
    def _ball_position_allowed(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> bool:
        match player_sign, ball_position:
            # Opposite logic from other cards, can pull the ball if not at the player's position.
            case (PlayerSign.white, BallPosition.white) | (PlayerSign.black, BallPosition.black):
                return False
            case _:
                return True

    @classmethod
    def _pull_ball(
        cls,
        player_sign: PlayerSign,
        ball_position: BallPosition,
    ) -> BallPosition:
        match player_sign, ball_position:
            case PlayerSign.white, BallPosition.middle:
                return BallPosition.white
            case PlayerSign.white, BallPosition.black:
                return BallPosition.middle
            case PlayerSign.black, BallPosition.middle:
                return BallPosition.black
            case PlayerSign.black, BallPosition.white:
                return BallPosition.middle
        raise RuntimeError(f"Cannot push ball. Player: {player_sign}, ball position: {ball_position}")


    @classmethod
    def _get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        card_index: int,
    ) -> list[Move]:
        return [
            Move(
                player_sign=player_sign,
                result_board=board.copy_board(),
                result_ball_position=cls._pull_ball(
                    player_sign=player_sign,
                    ball_position=board.ball_position,
                ),
                description=f"pull ball",
                used_card_index=card_index,
            ),
        ]
