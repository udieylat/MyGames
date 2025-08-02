class GameBoard {
    constructor() {
        this.board = this.initializeBoard();
        this.selectedTile = null;
        this.init();
    }

    initializeBoard() {
        // Create 5x5 board
        const board = [];
        for (let row = 0; row < 5; row++) {
            board[row] = [];
            for (let col = 0; col < 5; col++) {
                let piece = null;
                
                // White pawns on bottom row (row 4)
                if (row === 4) {
                    piece = 'white';
                }
                // Black pawns on top row (row 0)
                else if (row === 0) {
                    piece = 'black';
                }
                
                board[row][col] = {
                    piece: piece,
                    row: row,
                    col: col
                };
            }
        }
        return board;
    }

    init() {
        this.renderBoard();
        this.addEventListeners();
    }

    renderBoard() {
        const boardElement = document.getElementById('gameBoard');
        boardElement.innerHTML = '';

        for (let row = 0; row < 5; row++) {
            for (let col = 0; col < 5; col++) {
                const tile = this.board[row][col];
                const tileElement = this.createTileElement(tile, row, col);
                boardElement.appendChild(tileElement);
            }
        }
    }

    createTileElement(tile, row, col) {
        const tileElement = document.createElement('div');
        tileElement.className = `tile ${this.getTileColor(row, col)}`;
        tileElement.dataset.row = row;
        tileElement.dataset.col = col;

        if (tile.piece) {
            const pawnElement = document.createElement('div');
            pawnElement.className = `pawn ${tile.piece}`;
            pawnElement.textContent = '♟';
            tileElement.appendChild(pawnElement);
        }

        return tileElement;
    }

    getTileColor(row, col) {
        // Chess-like alternating pattern
        return (row + col) % 2 === 0 ? 'white' : 'black';
    }

    addEventListeners() {
        const boardElement = document.getElementById('gameBoard');
        boardElement.addEventListener('click', (e) => {
            const tile = e.target.closest('.tile');
            if (tile) {
                this.handleTileClick(tile);
            }
        });
    }

    handleTileClick(tileElement) {
        // Remove previous selection
        const previouslySelected = document.querySelector('.tile.selected');
        if (previouslySelected) {
            previouslySelected.classList.remove('selected');
        }

        // Select current tile
        tileElement.classList.add('selected');
        
        const row = parseInt(tileElement.dataset.row);
        const col = parseInt(tileElement.dataset.col);
        const tile = this.board[row][col];
        
        console.log(`Selected tile: Row ${row}, Col ${col}, Piece: ${tile.piece || 'empty'}`);
        
        // Update game info
        const gameInfo = document.querySelector('.game-info p');
        const colLetter = String.fromCharCode(65 + col); // A, B, C, D, E
        const rowNumber = 5 - row; // Convert to chess notation (1-5)
        gameInfo.textContent = `Selected: ${colLetter}${rowNumber} (${tile.piece || 'empty'})`;
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new GameBoard();
}); 