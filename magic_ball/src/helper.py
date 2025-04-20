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
        if BoardUtils.is_player_win(
            player_sign=PlayerSign.white,
            board=board.copy_board(),
        ):
            return GameStatus.white_win
        if BoardUtils.is_player_win(
            player_sign=PlayerSign.black,
            board=board.copy_board(),
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
                return GameStatus.white_defensive_win
            elif all(
                card.is_defensive
                for card in black_cards
            ):
                return GameStatus.black_defensive_win
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
                                target_tile=BoardUtils.indices_to_tile(col_i=col_i, row_i=row_i + 1),
                                board=board,
                            )
                        )
                    elif player_sign == PlayerSign.black and row_i > 0 and board[row_i - 1][col_i] == TileType.vacant:
                        available_push_moves.append(
                            cls.generate_push_move(
                                player_sign=PlayerSign.black,
                                target_tile=BoardUtils.indices_to_tile(col_i=col_i, row_i=row_i - 1),
                                board=board,
                            )
                        )

        available_card_moves = [
            move
            for card_index, card in enumerate(cards)
            for move in card.get_available_card_moves(
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
            board=board.copy_board(),
        )
        return Move(
            player_sign=player_sign,
            result_board=new_board,
            result_ball_position=board.ball_position,
            description=target_tile,  # f"push to target tile: {target_tile}",
        )

    @classmethod
    def move_pawn(
        cls,
        player_sign: PlayerSign,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
        board: BoardType,
    ) -> BoardType:
        """
        Notice: change input board argument in-place.
        """
        assert 0 <= source_col_i <= 4
        assert 0 <= source_row_i <= 4
        assert 0 <= target_col_i <= 4
        assert 0 <= target_row_i <= 4

        target_board_tile = board[target_row_i][target_col_i]
        if target_board_tile != TileType.vacant:
            raise InvalidMove(
                description=(
                    f"target tile {BoardUtils.indices_to_tile(col_i=target_col_i, row_i=target_row_i)} "
                    f"not vacant: {target_board_tile}"
                ),
            )

        source_board_tile = board[source_row_i][source_col_i]
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
        board = cls.eliminate_pawn(
            col_i=source_col_i,
            row_i=source_row_i,
            board=board,
        )
        board = cls.set_pawn_tile(
            player_sign=player_sign,
            col_i=target_col_i,
            row_i=target_row_i,
            board=board,
        )
        return board

    @classmethod
    def set_tile(
        cls,
        tile_type: TileType,
        col_i: int,
        row_i: int,
        board: BoardType,
        safe: bool = False,
    ) -> BoardType:
        """
        Notice: change input board argument in-place.
        """
        assert 0 <= col_i <= 4
        assert 0 <= row_i <= 4
        if not safe:
            assert board[row_i][col_i] != tile_type
        board[row_i][col_i] = tile_type
        return board

    @classmethod
    def set_pawn_tile(
        cls,
        player_sign: PlayerSign,
        col_i: int,
        row_i: int,
        board: BoardType,
    ) -> BoardType:
        return cls.set_tile(
            tile_type=(
                TileType.white
                if player_sign == PlayerSign.white
                else TileType.black
            ),
            col_i=col_i,
            row_i=row_i,
            board=board,
        )

    @classmethod
    def eliminate_pawn(
        cls,
        col_i: int,
        row_i: int,
        board: BoardType,
        safe: bool = False,
    ) -> BoardType:
        return cls.set_tile(
            tile_type=TileType.vacant,
            col_i=col_i,
            row_i=row_i,
            board=board,
            safe=safe,
        )

    @classmethod
    def get_pawn_indices(
        cls,
        player_sign: PlayerSign,
        board: Board | BoardType,
    ) -> list[tuple[int, int]]:
        return [
            (col_i, row_i)
            for col_i in range(5)
            for row_i in range(5)
            if BoardUtils.is_tile_player_pawn(
                player_sign=player_sign,
                tile=board[row_i][col_i],
            )
        ]

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
