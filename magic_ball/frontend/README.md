# Magic Ball Game - Web Interface

A simple web interface for the Magic Ball Game.

## Features

- 5x5 chess-like board
- White pawns on the bottom row
- Black pawns on the top row
- Click to select tiles
- Chess notation display (A1-E5)

## How to Run

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the local server:
   ```bash
   python server.py
   ```

3. Open your web browser and go to:
   ```
   http://localhost:8000
   ```

## Files

- `index.html` - Main HTML file
- `styles.css` - CSS styling for the game board
- `script.js` - JavaScript for game logic and board generation
- `server.py` - Simple HTTP server to serve the files locally

## Game Board Layout

The board uses chess notation:
- Columns: A, B, C, D, E (left to right)
- Rows: 1, 2, 3, 4, 5 (bottom to top)

- White pawns are on row 1 (bottom)
- Black pawns are on row 5 (top)
- Empty tiles are in the middle rows 