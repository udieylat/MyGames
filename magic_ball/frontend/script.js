class GameBoard {
    constructor() {
        this.board = this.initializeBoard();
        this.selectedTile = null;
        this.currentTurn = 'white'; // white goes first
        this.gameStatus = 'ongoing';
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
                    col: col,
                    hasMoved: false // Track if pawn has moved
                };
            }
        }
        return board;
    }

    init() {
        this.renderBoard();
        this.addEventListeners();
        this.updateGameInfo();
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
        const row = parseInt(tileElement.dataset.row);
        const col = parseInt(tileElement.dataset.col);
        const tile = this.board[row][col];

        // Clear previous selections and valid move indicators
        this.clearHighlights();

        // If clicking on a pawn of the current player's color
        if (tile.piece === this.currentTurn) {
            this.selectPawn(tileElement, tile);
        }
        // If clicking on a valid move destination
        else if (this.selectedTile && this.isValidMove(this.selectedTile, row, col)) {
            this.movePawn(this.selectedTile, row, col);
        }
        // If clicking on an empty tile or opponent's piece, deselect
        else {
            this.selectedTile = null;
        }

        this.updateGameInfo();
    }

    selectPawn(tileElement, tile) {
        this.selectedTile = tile;
        tileElement.classList.add('selected');
        
        // Highlight valid moves
        this.highlightValidMoves(tile);
    }

    highlightValidMoves(selectedTile) {
        const validMoves = this.getValidMoves(selectedTile);
        
        validMoves.forEach(move => {
            const tileElement = document.querySelector(`[data-row="${move.row}"][data-col="${move.col}"]`);
            if (tileElement) {
                tileElement.classList.add('valid-move');
            }
        });
    }

    clearHighlights() {
        // Remove all highlights
        document.querySelectorAll('.tile.selected, .tile.valid-move, .pawn.selected').forEach(el => {
            el.classList.remove('selected', 'valid-move');
        });
    }

    getValidMoves(tile) {
        const validMoves = [];
        
        if (!tile.piece || tile.piece !== this.currentTurn) {
            return validMoves;
        }

        const direction = tile.piece === 'white' ? -1 : 1; // White moves up, black moves down
        const newRow = tile.row + direction;

        // Check if the move is within bounds
        if (newRow >= 0 && newRow < 5) {
            const targetTile = this.board[newRow][tile.col];
            
            // Can only move to empty tiles (no capturing)
            if (targetTile.piece === null) {
                validMoves.push({
                    row: newRow,
                    col: tile.col
                });
            }
        }

        return validMoves;
    }

    isValidMove(fromTile, toRow, toCol) {
        const validMoves = this.getValidMoves(fromTile);
        return validMoves.some(move => move.row === toRow && move.col === toCol);
    }

    movePawn(fromTile, toRow, toCol) {
        // Update the board
        this.board[toRow][toCol].piece = fromTile.piece;
        this.board[toRow][toCol].hasMoved = true;
        this.board[fromTile.row][fromTile.col].piece = null;
        this.board[fromTile.row][fromTile.col].hasMoved = false;

        // Re-render the board
        this.renderBoard();
        
        // Switch turns
        this.currentTurn = this.currentTurn === 'white' ? 'black' : 'white';
        
        // Clear selection
        this.selectedTile = null;
        
        // Check for win conditions
        this.checkWinConditions();
    }

    hasAnyValidMoves(player) {
        for (let row = 0; row < 5; row++) {
            for (let col = 0; col < 5; col++) {
                const tile = this.board[row][col];
                if (tile.piece === player) {
                    const validMoves = this.getValidMoves(tile);
                    if (validMoves.length > 0) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    checkWinConditions() {
        // Check if any pawn has reached the opposite side
        let whiteWon = false;
        let blackWon = false;

        // Check if any white pawn reached the top row
        for (let col = 0; col < 5; col++) {
            if (this.board[0][col].piece === 'white') {
                whiteWon = true;
                break;
            }
        }

        // Check if any black pawn reached the bottom row
        for (let col = 0; col < 5; col++) {
            if (this.board[4][col].piece === 'black') {
                blackWon = true;
                break;
            }
        }

        if (whiteWon) {
            this.gameStatus = 'white_win';
            this.updateGameInfo();
        } else if (blackWon) {
            this.gameStatus = 'black_win';
            this.updateGameInfo();
        } else {
            // Check for draw - if current player has no valid moves
            if (!this.hasAnyValidMoves(this.currentTurn)) {
                this.gameStatus = 'draw';
                this.updateGameInfo();
            }
        }
    }

    updateGameInfo() {
        const turnIndicator = document.getElementById('turnIndicator');
        const gameStatus = document.getElementById('gameStatus');
        const moveInfo = document.getElementById('moveInfo');

        if (this.gameStatus === 'ongoing') {
            turnIndicator.textContent = `${this.currentTurn.charAt(0).toUpperCase() + this.currentTurn.slice(1)}'s Turn`;
            turnIndicator.className = `turn-indicator ${this.currentTurn}`;
            
            if (this.selectedTile) {
                const colLetter = String.fromCharCode(65 + this.selectedTile.col);
                const rowNumber = 5 - this.selectedTile.row;
                gameStatus.textContent = `Selected: ${colLetter}${rowNumber} (${this.selectedTile.piece})`;
                moveInfo.textContent = `${this.currentTurn.charAt(0).toUpperCase() + this.currentTurn.slice(1)} pawns can move one step forward`;
            } else {
                gameStatus.textContent = `Click on a ${this.currentTurn} pawn to select it`;
                moveInfo.textContent = `${this.currentTurn.charAt(0).toUpperCase() + this.currentTurn.slice(1)} pawns can move one step forward`;
            }
        } else if (this.gameStatus === 'white_win') {
            turnIndicator.textContent = 'White Wins!';
            turnIndicator.className = 'turn-indicator white';
            gameStatus.textContent = 'White pawn reached the top row!';
            moveInfo.textContent = 'Game Over';
        } else if (this.gameStatus === 'black_win') {
            turnIndicator.textContent = 'Black Wins!';
            turnIndicator.className = 'turn-indicator black';
            gameStatus.textContent = 'Black pawn reached the bottom row!';
            moveInfo.textContent = 'Game Over';
        } else if (this.gameStatus === 'draw') {
            turnIndicator.textContent = 'Game is a Draw!';
            turnIndicator.className = 'turn-indicator draw';
            gameStatus.textContent = 'No valid moves available';
            moveInfo.textContent = 'Game Over';
        }
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new GameBoard();
}); 