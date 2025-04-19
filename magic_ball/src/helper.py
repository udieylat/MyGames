from board import Board
from board_utils import BoardUtils
from move import PossibleMoveType, PushMove
from models import PlayerSign, TileType, GameStatus


class Helper:

    @classmethod
    def get_game_status(
        cls,
        board: Board,
        white_magic_cards: list = [],
        black_magic_cards: list = [],  # TODO: impl once ready with magic cards
    ) -> GameStatus:
        if cls._is_player_win(
            player_sign=PlayerSign.white,
            board=board,
        ):
            return GameStatus.white_win
        if cls._is_player_win(
            player_sign=PlayerSign.black,
            board=board,
        ):
            return GameStatus.black_win
        if cls._is_draw(
            board=board,
            white_magic_cards=white_magic_cards,
            black_magic_cards=black_magic_cards,
        ):  # TODO: impl also the defensive cards win condition
            return GameStatus.draw
        return GameStatus.ongoing

    @classmethod
    def get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
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

    @classmethod
    def _is_player_win(
        cls,
        player_sign: PlayerSign,
        board: Board,
    ) -> bool:
        if player_sign == PlayerSign.white:
            return any(
                board[4][col_i] == TileType.white
                for col_i in range(5)
            )
        return any(
            board[0][col_i] == TileType.black
            for col_i in range(5)
        )

    @classmethod
    def _is_draw(
        cls,
        board: Board,
        white_magic_cards: list,
        black_magic_cards: list,
    ) -> bool:
        white_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.white,
            board=board,
        )
        black_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.black,
            board=board,
        )
        return not white_available_push_moves and not black_available_push_moves
