from models import PlayerSign, TileType


class BoardUtils:

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
