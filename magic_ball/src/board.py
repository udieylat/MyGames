class Board:
    def __init__(self):
        self._board = self._init_board()

    @classmethod
    def _init_board(cls) -> list[list[str]]:
        board = [['.' for _ in range(5)] for _ in range(5)]
        board[0] = ['W', 'W', 'W', 'W', 'W']  # White pawns
        board[4] = ['B', 'B', 'B', 'B', 'B']  # Black pawns
        return board

    def display(self):
        print("\nBoard:")
        for row in self._board:
            print(' '.join(row))
        print()
