import random


# Initialize the board
def initialize_board():
    # 5x5 board with initial positions for white (W) and black (B)
    board = [['.' for _ in range(5)] for _ in range(5)]
    board[0] = ['W', 'W', 'W', 'W', 'W']  # White pawns
    board[4] = ['B', 'B', 'B', 'B', 'B']  # Black pawns
    return board


# Display the board
def display_board(board):
    print("\nBoard:")
    for row in board:
        print(' '.join(row))
    print()


# Move a pawn on the board
def move_pawn(board, start, end):
    x1, y1 = start
    x2, y2 = end
    if board[x1][y1] != '.':
        board[x1][y1] = '.'  # Vacate start position
        board[x2][y2] = 'W' if board[x1][y1] == 'W' else 'B'  # Move pawn
    return board


# Check for win condition
def check_win(board, player):
    front_row = 0 if player == 'W' else 4
    for i in range(5):
        if board[front_row][i] == player:
            return True
    return False


# Check for available moves for a player
def available_moves(board, player):
    moves = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                if i > 0 and board[i - 1][j] == '.':
                    moves.append(((i, j), (i - 1, j)))  # Move up
                if i < 4 and board[i + 1][j] == '.':
                    moves.append(((i, j), (i + 1, j)))  # Move down
    return moves


# AI Strategy: Simple greedy approach (pick the first available move)
def ai_move(board, player):
    moves = available_moves(board, player)
    if moves:
        move = random.choice(moves)  # Randomly choose from available moves
        return move
    return None


# Main game loop
def play_game():
    board = initialize_board()
    ball_position = 'M'  # Middle (M) to start
    turn = 'W'  # White player starts

    while True:
        display_board(board)

        if turn == 'W':
            print("White's turn:")
            move = ai_move(board, 'W')  # AI makes move
        else:
            print("Black's turn:")
            move = ai_move(board, 'B')  # AI makes move

        if move:
            start, end = move
            board = move_pawn(board, start, end)

        if check_win(board, 'W'):
            print("White wins!")
            break
        if check_win(board, 'B'):
            print("Black wins!")
            break

        # Change turn
        turn = 'B' if turn == 'W' else 'W'


# Start the game
play_game()
