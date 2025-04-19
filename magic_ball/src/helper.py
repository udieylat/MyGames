from board import Board, InvalidMove
from board_utils import BoardUtils
from cards.card import Card
from move import Move
from models import PlayerSign, TileType, GameStatus, BoardType


class Helper:

    @classmethod
    def get_game_status(
        cls,
        board: Board,
        white_cards: list[Card],
        black_cards: list[Card],
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
        if cls._no_available_moves(
            board=board,
            white_cards=white_cards,
            black_cards=black_cards,
        ):
            if all(
                card.is_defensive
                for card in white_cards
            ):
                return GameStatus.white_win
            elif all(
                card.is_defensive
                for card in black_cards
            ):
                return GameStatus.black_win
            return GameStatus.draw
        return GameStatus.ongoing

    @classmethod
    def get_available_moves(
        cls,
        player_sign: PlayerSign,
        board: Board,
        cards: list[Card],
    ) -> list[Move]:
        available_push_moves = []
        for row_i in range(5):
            for col_i in range(5):
                if BoardUtils.is_tile_player_pawn(
                    player_sign=player_sign,
                    tile=board[row_i][col_i],
                ):
                    if player_sign == PlayerSign.white and row_i < 4 and board[row_i + 1][col_i] == TileType.vacant:
                        available_push_moves.append(
                            cls.generate_push_move(
                                player_sign=PlayerSign.white,
                                target_tile=BoardUtils.indices_to_tile(row_i=row_i + 1, col_i=col_i),
                                board=board,
                            )
                        )
                    elif player_sign == PlayerSign.black and row_i > 0 and board[row_i - 1][col_i] == TileType.vacant:
                        available_push_moves.append(
                            cls.generate_push_move(
                                player_sign=PlayerSign.black,
                                target_tile=BoardUtils.indices_to_tile(row_i=row_i - 1, col_i=col_i),
                                board=board,
                            )
                        )

        available_card_moves = [
            move
            for card_index, card in enumerate(cards)
            for move in card.get_available_moves(
                player_sign=player_sign,
                board=board,
                card_index=card_index,
            )
        ]

        return available_push_moves + available_card_moves

    @classmethod
    def generate_push_move(
        cls,
        player_sign: PlayerSign,
        target_tile: str,
        board: Board,
    ) -> Move:
        col_i, row_i = BoardUtils.tile_index(
            tile=target_tile,
        )
        source_row_i = (
            row_i - 1
            if player_sign == PlayerSign.white
            else row_i + 1
        )
        new_board = cls.move_pawn(
            player_sign=player_sign,
            source_col_i=col_i,
            source_row_i=source_row_i,
            target_col_i=col_i,
            target_row_i=row_i,
            board=board,
        )
        return Move(
            player_sign=player_sign,
            result_board=new_board,
            result_ball_position=board.ball_position,
            description=f"push to target tile: {target_tile}",
        )

    @classmethod
    def move_pawn(
        cls,
        player_sign: PlayerSign,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
        board: Board,
    ) -> BoardType:
        assert 0 <= source_col_i <= 4
        assert 0 <= source_row_i <= 4
        assert 0 <= target_col_i <= 4
        assert 0 <= target_row_i <= 4

        new_board = board.copy_board()
        target_board_tile = new_board[target_row_i][target_col_i]
        if target_board_tile != TileType.vacant:
            raise InvalidMove(
                description=(
                    f"target tile {BoardUtils.indices_to_tile(col_i=target_col_i, row_i=target_row_i)} "
                    f"not vacant: {target_board_tile}"
                ),
            )

        source_board_tile = new_board[source_row_i][source_col_i]
        if not BoardUtils.is_tile_player_pawn(
            player_sign=player_sign,
            tile=source_board_tile,
        ):
            raise InvalidMove(
                description=(
                    f"source board tile is not a valid pawn: "
                    f"{BoardUtils.indices_to_tile(col_i=source_col_i, row_i=source_row_i)} = {source_board_tile}"
                ),
            )

        # Complete move
        new_board[source_row_i][source_col_i] = TileType.vacant
        new_board[target_row_i][target_col_i] = (
            TileType.white
            if player_sign == PlayerSign.white
            else TileType.black
        )
        return new_board

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
    def _no_available_moves(
        cls,
        board: Board,
        white_cards: list[Card],
        black_cards: list[Card],
    ) -> bool:
        white_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.white,
            board=board,
            cards=white_cards,
        )
        black_available_push_moves = Helper.get_available_moves(
            player_sign=PlayerSign.black,
            board=board,
            cards=black_cards,
        )
        return not white_available_push_moves and not black_available_push_moves
