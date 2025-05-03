from models import PlayerSign, TileType, BoardType


class BoardUtils:

    @classmethod
    def inverse_player_sign(
        cls,
        player_sign: PlayerSign,
    ) -> PlayerSign:
        return (
            PlayerSign.white
            if player_sign == PlayerSign.black
            else PlayerSign.black
        )

    @classmethod
    def is_player_win(
        cls,
        player_sign: PlayerSign,
        board: BoardType,
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
    def is_any_player_win(
        cls,
        board: BoardType,
    ) -> bool:
        return cls.is_player_win(
            player_sign=PlayerSign.white,
            board=board,
        ) or cls.is_player_win(
            player_sign=PlayerSign.black,
            board=board,
        )

    @classmethod
    def is_player_single_push_to_win(
        cls,
        player_sign: PlayerSign,
        board: BoardType,
    ) -> bool:
        if player_sign == PlayerSign.white:
            return any(
                board[3][col_i] == TileType.white and board[4][col_i] == TileType.vacant
                for col_i in range(5)
            )
        return any(
            board[1][col_i] == TileType.black and board[0][col_i] == TileType.vacant
            for col_i in range(5)
        )

    @classmethod
    def is_tile_player_pawn(
        cls,
        player_sign: PlayerSign,
        tile: str,
    ) -> bool:
        return (
            (player_sign == PlayerSign.white and tile == TileType.white)
            or (player_sign == PlayerSign.black and tile == TileType.black)
        )

    @classmethod
    def is_tile_opponent_pawn(
        cls,
        player_sign: PlayerSign,
        tile: str,
    ) -> bool:
        return (
            (player_sign == PlayerSign.white and tile == TileType.black)
            or (player_sign == PlayerSign.black and tile == TileType.white)
        )

    @classmethod
    def tile_index(
        cls,
        tile: str,
    ) -> tuple[int, int]:
        return (
            "ABCDE".index(tile[0]),
            "12345".index(tile[1]),
        )

    @classmethod
    def indices_to_tile(
        cls,
        col_i: int,
        row_i: int,
    ) -> str:
        return "ABCDE"[col_i] + "12345"[row_i]

    @classmethod
    def tile_to_player_sign(
        cls,
        tile: str,
    ) -> PlayerSign:
        match tile:
            case TileType.white:
                return PlayerSign.white
            case TileType.black:
                return PlayerSign.black
        raise RuntimeError(f"Not a pawn tile: {tile}")

    @classmethod
    def get_neighbor_tiles_indices(
        cls,
        col_i: int,
        row_i: int,
    ) -> list[tuple[int, int]]:
        all_neighbor_tiles_indices = [
            (col_i, row_i + 1),
            (col_i, row_i - 1),
            (col_i + 1, row_i),
            (col_i - 1, row_i),
        ]
        return [
            (col_i, row_i)
            for col_i, row_i in all_neighbor_tiles_indices
            if 0 <= col_i <= 4 and 0 <= row_i <= 4
        ]

    @classmethod
    def get_diagonal_neighbor_tiles_indices(
        cls,
        col_i: int,
        row_i: int,
    ) -> list[tuple[int, int]]:
        all_neighbor_tiles_indices = [
            (col_i + 1, row_i + 1),
            (col_i + 1, row_i - 1),
            (col_i - 1, row_i - 1),
            (col_i - 1, row_i + 1),
        ]
        return [
            (col_i, row_i)
            for col_i, row_i in all_neighbor_tiles_indices
            if 0 <= col_i <= 4 and 0 <= row_i <= 4
        ]

    @classmethod
    def describe_pawn_move(
        cls,
        card_name: str,
        source_col_i: int,
        source_row_i: int,
        target_col_i: int,
        target_row_i: int,
    ) -> str:
        return (
            f"{card_name}: "
            f"{BoardUtils.indices_to_tile(col_i=source_col_i, row_i=source_row_i)}->"
            f"{BoardUtils.indices_to_tile(col_i=target_col_i, row_i=target_row_i)}"
        )
