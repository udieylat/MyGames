#!/usr/bin/env python3
"""
Test script to verify board initialization works correctly.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from game_manager import GameManager
from game_config import GameConfig

def test_board_initialization():
    """Test that the board initializes correctly"""
    try:
        print("Testing board initialization...")
        
        # Create game config
        config = GameConfig()
        
        # Create new game manager
        game_manager = GameManager.new(config=config)
        
        print(f"Game manager created successfully")
        print(f"Board: {game_manager._board._board}")
        print(f"Ball position: {game_manager._board.ball_position}")
        
        # Check board structure
        board = game_manager._board._board
        if len(board) != 5:
            print(f"ERROR: Board has {len(board)} rows, expected 5")
            return False
            
        for i, row in enumerate(board):
            if len(row) != 5:
                print(f"ERROR: Row {i} has {len(row)} columns, expected 5")
                return False
            print(f"Row {i}: {row}")
        
        # Check that white pawns are on top row (row 0)
        if not all(tile == 'W' for tile in board[0]):
            print("ERROR: White pawns not on top row")
            return False
            
        # Check that black pawns are on bottom row (row 4)
        if not all(tile == 'B' for tile in board[4]):
            print("ERROR: Black pawns not on bottom row")
            return False
            
        # Check that middle rows are vacant
        for i in range(1, 4):
            if not all(tile == '.' for tile in board[i]):
                print(f"ERROR: Row {i} is not vacant")
                return False
        
        print("✓ Board initialization test passed!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_board_initialization() 