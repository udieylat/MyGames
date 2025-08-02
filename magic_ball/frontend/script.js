class GameBoard {
    constructor() {
        this.gameState = null;
        this.selectedCard = null;
        this.selectedTile = null;
        this.validMoves = [];
        this.moveHistory = [];
        this.init();
    }

    async init() {
        await this.startNewGame();
        this.addEventListeners();
    }

    async startNewGame() {
        try {
            console.log('Starting new game...');
            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            console.log('New game response:', data);
            
            if (data.success) {
                this.gameState = data.game_state;
                console.log('Game state:', this.gameState);
                this.renderGame();
            } else {
                console.error('Failed to start new game:', data.error);
            }
        } catch (error) {
            console.error('Error starting new game:', error);
        }
    }

    async getGameState() {
        try {
            const response = await fetch('/api/game/state');
            const data = await response.json();
            console.log('Get game state response:', data);
            if (data.success) {
                this.gameState = data;
                return data;
            }
        } catch (error) {
            console.error('Error getting game state:', error);
        }
        return null;
    }

    async makeMove(moveData) {
        try {
            const response = await fetch('/api/game/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(moveData)
            });
            
            const data = await response.json();
            if (data.success) {
                this.gameState = data.game_state;
                
                // Add move to history
                this.addMoveToHistory(moveData, data.message);
                
                this.renderGame();
                return true;
            } else {
                console.error('Move failed:', data.error);
                return false;
            }
        } catch (error) {
            console.error('Error making move:', error);
            return false;
        }
    }

    addMoveToHistory(moveData, description) {
        const moveNumber = Math.floor(this.moveHistory.length / 2) + 1;
        const player = this.gameState.current_player === 'white' ? 'White' : 'Black';
        
        let moveDescription = '';
        if (moveData.type === 'push') {
            moveDescription = `${player} pushes to ${moveData.target_tile}`;
        } else if (moveData.type === 'card') {
            moveDescription = `${player} plays card (${moveData.card_index})`;
        } else if (moveData.type === 'pass') {
            moveDescription = `${player} passes turn`;
        }
        
        this.moveHistory.push({
            number: moveNumber,
            player: player,
            description: moveDescription,
            backendDescription: description
        });
        
        this.renderMoveHistory();
    }

    renderMoveHistory() {
        const movesList = document.getElementById('movesList');
        movesList.innerHTML = '';
        
        this.moveHistory.forEach((move, index) => {
            const moveEntry = document.createElement('div');
            moveEntry.className = 'move-entry';
            
            const moveNumber = document.createElement('span');
            moveNumber.className = 'move-number';
            moveNumber.textContent = `${move.number}.`;
            
            const moveDescription = document.createElement('span');
            moveDescription.className = 'move-description';
            moveDescription.textContent = move.description;
            
            moveEntry.appendChild(moveNumber);
            moveEntry.appendChild(moveDescription);
            movesList.appendChild(moveEntry);
        });
    }

    async getValidMoves() {
        try {
            const response = await fetch('/api/game/valid-moves');
            const data = await response.json();
            if (data.success) {
                this.validMoves = data.valid_moves;
                return data.valid_moves;
            }
        } catch (error) {
            console.error('Error getting valid moves:', error);
        }
        return [];
    }

    renderGame() {
        console.log('Rendering game with state:', this.gameState);
        this.renderBoard();
        this.renderCards();
        this.updateGameInfo();
        this.updateMagicBall();
    }

    renderBoard() {
        const boardElement = document.getElementById('gameBoard');
        boardElement.innerHTML = '';

        if (!this.gameState || !this.gameState.board) {
            console.error('No game state or board data available');
            return;
        }

        console.log('Rendering board with data:', this.gameState.board);

        // Flip the board so white pawns are on bottom and black on top
        for (let row = 0; row < 5; row++) {
            for (let col = 0; col < 5; col++) {
                // Flip the row index: row 0 becomes row 4, row 4 becomes row 0
                const flippedRow = 4 - row;
                const tile = this.gameState.board[flippedRow][col];
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

        if (tile) {
            const pawnElement = document.createElement('div');
            pawnElement.className = `pawn ${tile}`;
            pawnElement.textContent = '♟';
            tileElement.appendChild(pawnElement);
        }

        return tileElement;
    }

    getTileColor(row, col) {
        return (row + col) % 2 === 0 ? 'white' : 'black';
    }

    renderCards() {
        if (!this.gameState) return;

        // Render white cards
        const whiteCardsList = document.getElementById('whiteCardsList');
        whiteCardsList.innerHTML = '';
        
        if (this.gameState.white_cards) {
            this.gameState.white_cards.forEach((cardName, index) => {
                const cardElement = this.createCardElement(cardName, index, 'white');
                whiteCardsList.appendChild(cardElement);
            });
        }

        // Render black cards
        const blackCardsList = document.getElementById('blackCardsList');
        blackCardsList.innerHTML = '';
        
        if (this.gameState.black_cards) {
            this.gameState.black_cards.forEach((cardName, index) => {
                const cardElement = this.createCardElement(cardName, index, 'black');
                blackCardsList.appendChild(cardElement);
            });
        }
    }

    createCardElement(cardName, index, player) {
        const cardElement = document.createElement('button');
        cardElement.className = 'card';
        cardElement.textContent = cardName;
        cardElement.dataset.cardIndex = index;
        cardElement.dataset.player = player;
        
        cardElement.addEventListener('click', () => this.selectCard(cardElement, cardName, index, player));
        
        return cardElement;
    }

    selectCard(cardElement, cardName, index, player) {
        // Clear previous card selection
        document.querySelectorAll('.card.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // Select this card
        cardElement.classList.add('selected');
        this.selectedCard = { name: cardName, index: index, player: player };

        // Get valid moves for this card
        this.getValidMovesForCard(index);
    }

    async getValidMovesForCard(cardIndex) {
        try {
            const response = await fetch('/api/game/cards');
            const data = await response.json();
            if (data.success) {
                const card = data.cards.find(c => c.index === cardIndex);
                if (card) {
                    console.log(`Card ${card.name}: ${card.description}`);
                }
            }
        } catch (error) {
            console.error('Error getting card moves:', error);
        }
    }

    updateMagicBall() {
        if (!this.gameState || !this.gameState.ball_position) return;

        const magicBall = document.getElementById('magicBall');
        const position = this.gameState.ball_position;
        
        // Update magic ball appearance based on position
        magicBall.className = `magic-ball ${position}`;
        
        // Add position indicator
        let positionText = '';
        switch (position) {
            case 'white':
                positionText = 'W';
                break;
            case 'black':
                positionText = 'B';
                break;
            case 'middle':
                positionText = 'M';
                break;
        }
        
        // Update or create position indicator
        let indicator = magicBall.querySelector('.position-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'position-indicator';
            magicBall.appendChild(indicator);
        }
        indicator.textContent = positionText;
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

    async handleTileClick(tileElement) {
        const row = parseInt(tileElement.dataset.row);
        const col = parseInt(tileElement.dataset.col);
        
        // Clear previous highlights
        this.clearHighlights();

        // Check if this is a pawn of the current player
        const flippedRow = 4 - row;
        const tile = this.gameState.board[flippedRow][col];
        const currentPlayer = this.gameState.current_player;
        
        if (tile === currentPlayer) {
            // Select this pawn
            this.selectPawn(tileElement, row, col);
        } else if (this.selectedTile) {
            // Try to move the selected pawn to this tile
            await this.movePawnToTile(row, col);
        } else if (this.selectedCard) {
            // Try to play the selected card
            await this.playCardMove(row, col);
        } else {
            // Try to make a push move
            await this.makePushMove(row, col);
        }
    }

    selectPawn(tileElement, row, col) {
        // Clear previous selections
        document.querySelectorAll('.tile.selected, .pawn.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // Select this pawn
        tileElement.classList.add('selected');
        this.selectedTile = { row: row, col: col };

        // Highlight valid moves for this pawn
        this.highlightValidMovesForPawn(row, col);
    }

    highlightValidMovesForPawn(row, col) {
        // For now, highlight the tile in front of the pawn
        const currentPlayer = this.gameState.current_player;
        const direction = currentPlayer === 'white' ? -1 : 1; // White moves up, black moves down
        const targetRow = row + direction;

        if (targetRow >= 0 && targetRow < 5) {
            const targetTile = document.querySelector(`[data-row="${targetRow}"][data-col="${col}"]`);
            if (targetTile) {
                // Check if the target tile is empty
                const flippedTargetRow = 4 - targetRow;
                const tileContent = this.gameState.board[flippedTargetRow][col];
                
                if (!tileContent) {
                    targetTile.classList.add('valid-move');
                }
            }
        }
    }

    async movePawnToTile(targetRow, targetCol) {
        if (!this.selectedTile) return;

        const sourceTile = this.coordinatesToTile(this.selectedTile.row, this.selectedTile.col);
        const targetTile = this.coordinatesToTile(targetRow, targetCol);
        
        const moveData = {
            type: 'push',
            target_tile: targetTile
        };

        const success = await this.makeMove(moveData);
        if (success) {
            this.selectedTile = null;
        }
    }

    async playCardMove(row, col) {
        if (!this.selectedCard) return;

        // Convert coordinates to tile notation
        const tile = this.coordinatesToTile(row, col);
        
        // For now, we'll use a simple card move
        // In a full implementation, you'd need to get the specific move index
        const moveData = {
            type: 'card',
            card_index: this.selectedCard.index,
            move_index: 0  // This would need to be determined based on available moves
        };

        const success = await this.makeMove(moveData);
        if (success) {
            this.selectedCard = null;
        }
    }

    async makePushMove(row, col) {
        const tile = this.coordinatesToTile(row, col);
        
        const moveData = {
            type: 'push',
            target_tile: tile
        };

        await this.makeMove(moveData);
    }

    coordinatesToTile(row, col) {
        const letters = ['A', 'B', 'C', 'D', 'E'];
        const numbers = ['5', '4', '3', '2', '1'];
        return letters[col] + numbers[row];
    }

    clearHighlights() {
        document.querySelectorAll('.tile.selected, .tile.valid-move, .card.selected, .pawn.selected').forEach(el => {
            el.classList.remove('selected', 'valid-move');
        });
    }

    updateGameInfo() {
        if (!this.gameState) return;

        const turnIndicator = document.getElementById('turnIndicator');
        const gameStatus = document.getElementById('gameStatus');
        const moveInfo = document.getElementById('moveInfo');
        const menuButtonContainer = document.getElementById('menuButtonContainer');

        const currentPlayer = this.gameState.current_player;
        const gameStatusValue = this.gameState.game_status;

        // Convert integer game status to string for comparison
        let gameStatusString = '';
        switch (gameStatusValue) {
            case 1:
                gameStatusString = 'ongoing';
                break;
            case 2:
                gameStatusString = 'white_win';
                break;
            case 3:
                gameStatusString = 'black_win';
                break;
            case 4:
                gameStatusString = 'draw';
                break;
            default:
                gameStatusString = 'ongoing';
        }

        if (gameStatusString === 'ongoing') {
            turnIndicator.textContent = `${currentPlayer.charAt(0).toUpperCase() + currentPlayer.slice(1)}'s Turn`;
            turnIndicator.className = `turn-indicator ${currentPlayer}`;
            menuButtonContainer.style.display = 'none';
            
            gameStatus.textContent = `Current player: ${currentPlayer}`;
            moveInfo.textContent = 'Select a card or make a push move';
        } else {
            // Game is over
            let resultText = '';
            let statusText = '';
            
            if (gameStatusString === 'white_win') {
                resultText = 'White Wins!';
                statusText = 'White has won the game!';
            } else if (gameStatusString === 'black_win') {
                resultText = 'Black Wins!';
                statusText = 'Black has won the game!';
            } else if (gameStatusString === 'draw') {
                resultText = 'Game is a Draw!';
                statusText = 'The game ended in a draw!';
            }
            
            turnIndicator.textContent = resultText;
            turnIndicator.className = 'turn-indicator draw';
            gameStatus.textContent = statusText;
            moveInfo.textContent = 'Game Over';
            menuButtonContainer.style.display = 'block';
        }
    }
}

// Global function to go back to menu
function backToMenu() {
    window.location.href = 'index.html';
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new GameBoard();
}); 