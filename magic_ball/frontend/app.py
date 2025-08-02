#!/usr/bin/env python3
"""
Flask backend API for the Magic Ball Game web interface.
Integrates with the existing Python game engine.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

from game_manager import GameManager
from game_config import GameConfig
from models import PlayerSign, GameStatus, TileType
from board_utils import BoardUtils

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Global game instance
game_manager = None

@app.route('/')
def index():
    """Serve the main menu page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start a new game"""
    global game_manager
    
    try:
        data = request.get_json() or {}
        
        # Create game config
        config = GameConfig()
        
        # Create new game manager
        game_manager = GameManager.new(config=config)
        
        print(f"Game manager created: {game_manager}")
        print(f"Board: {game_manager._board._board}")
        print(f"Ball position: {game_manager._board.ball_position}")
        
        return jsonify({
            'success': True,
            'message': 'New game started',
            'game_state': get_game_state()
        })
    except Exception as e:
        print(f"Error creating new game: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_game_state():
    """Get current game state"""
    global game_manager
    
    if not game_manager:
        return {
            'success': False,
            'error': 'No active game'
        }
    
    try:
        # Get board state
        board = game_manager._board._board
        ball_position = game_manager._board.ball_position.value
        
        print(f"Board data: {board}")
        print(f"Ball position: {ball_position}")
        
        # Convert board to frontend format
        board_state = []
        for row in board:
            board_row = []
            for tile in row:
                # Convert TileType enum to string value
                tile_value = tile.value if hasattr(tile, 'value') else str(tile)
                if tile_value == 'W':
                    board_row.append('white')
                elif tile_value == 'B':
                    board_row.append('black')
                else:
                    board_row.append(None)
            board_state.append(board_row)
        
        print(f"Converted board state: {board_state}")
        
        # Get current player
        current_player = game_manager._player_turn.value
        
        # Get game status
        game_status = game_manager.game_status.value
        
        # Get player cards
        white_cards = [card.name for card in game_manager._white_player.cards if not card.already_used]
        black_cards = [card.name for card in game_manager._black_player.cards if not card.already_used]
        
        return {
            'success': True,
            'board': board_state,
            'ball_position': ball_position,
            'current_player': current_player,
            'game_status': game_status,
            'white_cards': white_cards,
            'black_cards': black_cards,
            'white_cards_count': len(white_cards),
            'black_cards_count': len(black_cards)
        }
    except Exception as e:
        print(f"Error getting game state: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/api/game/state', methods=['GET'])
def get_game_state_endpoint():
    """Get current game state"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        # Get board state
        board = game_manager._board._board
        ball_position = game_manager._board.ball_position.value
        
        # Convert board to frontend format
        board_state = []
        for row in board:
            board_row = []
            for tile in row:
                # Convert TileType enum to string value
                tile_value = tile.value if hasattr(tile, 'value') else str(tile)
                if tile_value == 'W':
                    board_row.append('white')
                elif tile_value == 'B':
                    board_row.append('black')
                else:
                    board_row.append(None)
            board_state.append(board_row)
        
        # Get current player
        current_player = game_manager._player_turn.value
        
        # Get game status
        game_status = game_manager.game_status.value
        
        # Get player cards
        white_cards = [card.name for card in game_manager._white_player.cards if not card.already_used]
        black_cards = [card.name for card in game_manager._black_player.cards if not card.already_used]
        
        return jsonify({
            'success': True,
            'board': board_state,
            'ball_position': ball_position,
            'current_player': current_player,
            'game_status': game_status,
            'white_cards': white_cards,
            'black_cards': black_cards,
            'white_cards_count': len(white_cards),
            'black_cards_count': len(black_cards)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/move', methods=['POST'])
def make_move():
    """Make a move in the game"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        data = request.get_json()
        move_type = data.get('type')
        
        if move_type == 'push':
            target_tile = data.get('target_tile')
            game_manager.push(target_tile)
        elif move_type == 'card':
            card_index = data.get('card_index')
            move_index = data.get('move_index')
            game_manager.play_card(card_index, move_index)
        elif move_type == 'pass':
            game_manager.pass_turn()
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid move type'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Move made successfully',
            'game_state': get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/valid-moves', methods=['GET'])
def get_valid_moves():
    """Get valid moves for the current player"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        # Get current player
        current_player = game_manager._get_player()
        
        # Get available moves
        available_moves = []
        
        # Check for push moves
        for row in range(5):
            for col in range(5):
                tile = BoardUtils.coordinates_to_tile(row, col)
                try:
                    # Try to generate a push move
                    move = BoardUtils.generate_push_move(
                        player_sign=game_manager._player_turn,
                        target_tile=tile,
                        board=game_manager._board
                    )
                    available_moves.append({
                        'type': 'push',
                        'target_tile': tile,
                        'description': f'Push to {tile}'
                    })
                except:
                    pass
        
        # Check for card moves
        for i, card in enumerate(current_player.cards):
            if not card.already_used:
                card_moves = game_manager._get_available_card_moves(i)
                for j, move in enumerate(card_moves):
                    available_moves.append({
                        'type': 'card',
                        'card_index': i,
                        'move_index': j,
                        'description': f'{card.name}: {move.description}'
                    })
        
        return jsonify({
            'success': True,
            'valid_moves': available_moves
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/cards', methods=['GET'])
def get_player_cards():
    """Get current player's cards"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        current_player = game_manager._get_player()
        cards = []
        
        for i, card in enumerate(current_player.cards):
            if not card.already_used:
                cards.append({
                    'index': i,
                    'name': card.name,
                    'description': card.description
                })
        
        return jsonify({
            'success': True,
            'cards': cards
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Magic Ball Game API server...")
    print("Access the game at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
