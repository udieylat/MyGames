from board_utils import BoardUtils
from move import PossibleMoveType, PushMove
from models import PlayerSign, TileType


class Helper:
    @classmethod
    def get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: list[list[str]],
        # ball_position,
        # magic_cards: list,
    ) -> list[PossibleMoveType]:
        available_moves = []
        for row_i in range(5):
            for col_i in range(5):
                if BoardUtils.is_tile_player_pawn(
                    player_sign=player_sign,
                    tile=board[row_i][col_i],
                ):
                    if player_sign == PlayerSign.white and row_i < 4 and board[row_i + 1][col_i] == TileType.vacant:
                        available_moves.append(
                            PushMove(
                                player_sign=PlayerSign.white,
                                target_tile=BoardUtils.indices_to_tile(row_i=row_i + 1, col_i=col_i),
                            )
                        )
                    elif player_sign == PlayerSign.black and row_i > 0 and board[row_i - 1][col_i] == TileType.vacant:
                        available_moves.append(
                            PushMove(
                                player_sign=PlayerSign.white,
                                target_tile=BoardUtils.indices_to_tile(row_i=row_i - 1, col_i=col_i),
                            )
                        )

        # TODO: magic cards, ball position, etc

        return available_moves
