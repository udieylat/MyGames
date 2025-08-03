class GameBoard {
    constructor() {
        this.gameState = null;
        this.selectedCard = null;
        this.selectedTile = null;
        this.validMoves = [];
        this.moveHistory = [];
        this.cardMoves = [];
        this.gameType = null;
        this.humanPlayerSide = null;
        
        // Store this instance globally for access by startNewGame
        window.currentGameBoard = this;
        
        this.init();
    }

    async init() {
        await this.startNewGame();
        this.addEventListeners();
    }

    async startNewGame() {
        try {
            console.log('Starting new game...');
            
            // Get game type and player side from session storage
            this.gameType = sessionStorage.getItem('gameType') || 'human_vs_human';
            this.humanPlayerSide = sessionStorage.getItem('playerSide') || 'white';
            
            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    game_type: this.gameType,
                    human_player_side: this.humanPlayerSide
                })
            });
            
            const data = await response.json();
            console.log('New game response:', data);
            
            if (data.success) {
                this.gameState = data.game_state;
                this.gameType = data.game_state.game_type;
                this.humanPlayerSide = data.game_state.human_player_side;
                console.log('Game state:', this.gameState);
                console.log('Game type:', this.gameType);
                console.log('Human player side:', this.humanPlayerSide);
                this.renderGame();
                
                // If it's an AI game and AI goes first, make AI move
                if (this.gameType === 'human_vs_ai' && this.humanPlayerSide === 'black') {
                    await this.makeAIMove();
                }
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
                this.gameType = data.game_type;
                this.humanPlayerSide = data.human_player_side;
                return data;
            }
        } catch (error) {
            console.error('Error getting game state:', error);
        }
        return null;
    }

    async makeMove(moveData) {
        try {
            console.log('=== FRONTEND: PLAYER MOVE ===');
            console.log('Move data:', moveData);
            
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
                this.addMoveToHistory(moveData, data.move_description);
                
                console.log('Move successful, new game state:', this.gameState);
                this.renderGame();
                
                // If it's an AI game and human just moved, make AI move after delay
                if (this.gameType === 'human_vs_ai' && this.isAITurn()) {
                    setTimeout(async () => {
                        await this.makeAIMove();
                    }, 500); // 0.5 second delay
                }
                
                console.log('=== END FRONTEND: PLAYER MOVE ===');
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

    async makeAIMove() {
        try {
            console.log('=== FRONTEND: AI MOVE ===');
            console.log('Making AI move...');
            
            const response = await fetch('/api/game/ai-move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('Successful AI move:', data.move_description);
                this.gameState = data.game_state;
                
                // Add AI move to history with detailed description
                this.addMoveToHistory({ type: 'ai' }, data.move_description);
                
                console.log('AI move successful, new game state:', this.gameState);
                this.renderGame();
                
                console.log('=== END FRONTEND: AI MOVE ===');
                return true;
            } else {
                console.error('AI move failed:', data.error);
                return false;
            }
        } catch (error) {
            console.error('Error making AI move:', error);
            return false;
        }
    }

    isAITurn() {
        if (this.gameType !== 'human_vs_ai') return false;
        
        const currentPlayer = this.gameState.current_player;
        const aiSide = this.humanPlayerSide === 'white' ? 'black' : 'white';
        
        return currentPlayer === aiSide;
    }

    isHumanTurn() {
        if (this.gameType !== 'human_vs_ai') return true;
        
        const currentPlayer = this.gameState.current_player;
        return currentPlayer === this.humanPlayerSide;
    }

    addMoveToHistory(moveData, description) {
        const moveNumber = Math.floor(this.moveHistory.length / 2) + 1;
        let player = 'Unknown';
        
        // It's the opposite since the move was already completed so it's the next player's turn.
        player = this.gameState.current_player === 'black' ? 'White' : 'Black';
        
        this.moveHistory.push({
            number: moveNumber,
            player: player,
            description: description,
            timestamp: new Date().toLocaleTimeString()
        });
        
        console.log('Move history updated:', this.moveHistory);
        
        this.renderMoveHistory();
    }

    renderMoveHistory() {
        const movesList = document.getElementById('movesList');
        movesList.innerHTML = '';
        
        const totalMoves = this.moveHistory.length;
        const isOdd = totalMoves % 2 === 1;
        const pairsToShow = isOdd ? Math.floor(totalMoves / 2) + 1 : totalMoves / 2;
        
        for (let i = 0; i < pairsToShow; i++) {
            const moveEntry = document.createElement('div');
            moveEntry.className = 'move-entry';
            
            const moveNumber = document.createElement('span');
            moveNumber.className = 'move-number';
            moveNumber.textContent = `${i + 1}.`;
            
            const whiteMove = document.createElement('span');
            whiteMove.className = 'move-description white-move';
            whiteMove.textContent = this.moveHistory[i * 2]?.description || '';
            
            const separator = document.createElement('span');
            separator.className = 'move-separator';
            separator.textContent = ' | ';
            
            const blackMove = document.createElement('span');
            blackMove.className = 'move-description black-move';
            blackMove.textContent = this.moveHistory[i * 2 + 1]?.description || '';
            
            moveEntry.appendChild(moveNumber);
            moveEntry.appendChild(whiteMove);
            moveEntry.appendChild(separator);
            moveEntry.appendChild(blackMove);
            movesList.appendChild(moveEntry);
        }
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

        // Create a grid layout for the entire board
        boardElement.style.display = 'grid';
        boardElement.style.gridTemplateColumns = '30px repeat(5, 1fr)';
        boardElement.style.gridTemplateRows = 'repeat(5, 1fr) 30px';
        boardElement.style.gap = '0px';

        // Add row labels (5, 4, 3, 2, 1)
        for (let row = 0; row < 5; row++) {
            const rowLabel = document.createElement('div');
            rowLabel.className = 'board-label row-label';
            rowLabel.textContent = 5 - row; // 5, 4, 3, 2, 1
            rowLabel.style.gridColumn = '1';
            rowLabel.style.gridRow = row + 1;
            boardElement.appendChild(rowLabel);
        }

        // Create tiles container with brown frame
        const tilesContainer = document.createElement('div');
        tilesContainer.className = 'tiles-container';
        tilesContainer.style.gridColumn = '2 / 7';
        tilesContainer.style.gridRow = '1 / 6';
        
        // Add tiles to the container
        for (let row = 0; row < 5; row++) {
            for (let col = 0; col < 5; col++) {
                // Flip the row index: row 0 becomes row 4, row 4 becomes row 0
                const flippedRow = 4 - row;
                const tile = this.gameState.board[flippedRow][col];
                const tileElement = this.createTileElement(tile, row, col);
                tilesContainer.appendChild(tileElement);
            }
        }
        boardElement.appendChild(tilesContainer);

        // Add column labels (A-E) at the bottom
        for (let col = 0; col < 5; col++) {
            const label = document.createElement('div');
            label.className = 'board-label column-label';
            label.textContent = String.fromCharCode(65 + col); // A, B, C, D, E
            label.style.gridColumn = col + 2;
            label.style.gridRow = 6;
            boardElement.appendChild(label);
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
            this.gameState.white_cards.forEach((card, index) => {
                const cardElement = this.createCardElement(card, index, 'white');
                whiteCardsList.appendChild(cardElement);
            });
        }

        // Render black cards
        const blackCardsList = document.getElementById('blackCardsList');
        blackCardsList.innerHTML = '';
        
        if (this.gameState.black_cards) {
            this.gameState.black_cards.forEach((card, index) => {
                const cardElement = this.createCardElement(card, index, 'black');
                blackCardsList.appendChild(cardElement);
            });
        }
    }

    createCardElement(card, index, player) {
        const cardElement = document.createElement('button');
        cardElement.className = 'card';
        
        // Check if this is an AI card in an AI game
        const isAICard = this.gameType === 'human_vs_ai' && player !== this.humanPlayerSide;
        const isUsed = card.already_used;
        
        // Show card name or "???" for AI cards (reveal if used)
        const displayName = (isAICard && !isUsed) ? '???' : card.name;
        
        cardElement.textContent = displayName;
        cardElement.title = (isAICard && !isUsed) ? '???' : card.description;
        cardElement.dataset.cardIndex = index;
        cardElement.dataset.player = player;
        
        // Add used class if card is already used
        if (isUsed) {
            cardElement.classList.add('used');
        }
        
        cardElement.addEventListener('click', () => this.selectCard(cardElement, card, index, player));
        
        return cardElement;
    }

    async selectCard(cardElement, card, index, player) {
        // Check if game is over
        if (this.gameState.game_status !== 1) {
            console.log('Game is over, ignoring card selection');
            return;
        }
        
        // If it's an AI game and not human's turn, ignore card selection
        if (this.gameType === 'human_vs_ai' && !this.isHumanTurn()) {
            console.log('Not human turn, ignoring card selection');
            return;
        }
        
        // Check if card is already used
        if (card.already_used) {
            console.log('Card is already used, ignoring selection');
            return;
        }
        
        // Clear previous card selection
        document.querySelectorAll('.card.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // Select this card
        cardElement.classList.add('selected');
        this.selectedCard = { name: card.name, index: index, player: player };

        console.log(`Get card ${card.name} available moves, index ${index}, player ${player}`);

        // Get valid moves for this card
        await this.getCardMoves(index);

        // Highlight the selected card with enhanced visual feedback (only for unused cards)
        if (!card.already_used) {
            cardElement.style.transform = 'scale(1.1)';
            cardElement.style.boxShadow = '0 0 10px rgba(255, 255, 0, 0.8)';
            cardElement.style.border = '2px solid #ffd700';
        }
    }

    async getCardMoves(cardIndex) {
        try {
            const response = await fetch(`/api/game/card-moves/${cardIndex}`);
            const data = await response.json();
            if (data.success) {
                this.cardMoves = data.moves;
                console.log(`Selected card ${data.card_name}, index ${cardIndex}: ${data.card_description}`);
                console.log('Available moves:', this.cardMoves);
                
                // Highlight valid moves on the board
                this.highlightCardMoves();
            }
        } catch (error) {
            console.error('Error getting card moves:', error);
        }
    }

    highlightCardMoves() {
        // Clear previous highlights
        this.clearHighlights();
        
        // Track state for two-click flow
        this.currentHighlightState = 'tile_marker_1';
        this.tempMovesList = [];
        
        // Check if we have moves with tile_marker_2 (option 1) or only tile_marker_1 (option 2)
        const hasTileMarker2 = this.cardMoves.some(move => move.tile_marker_2 !== null);
        
        if (hasTileMarker2) {
            // Option 1: Both tile_marker_1 and tile_marker_2 are not null
            this.highlightTileMarkers1();
        } else {
            // Option 2: Only tile_marker_1 is not null
            this.highlightTileMarkers1();
        }
        // TODO: fire case, where both tile_marker_1 and tile_marker_2 are null
    }
    
    highlightTileMarkers1() {
        // Get unique tile_marker_1 values
        const tileMarkers1 = [...new Set(this.cardMoves.map(move => move.tile_marker_1).filter(tile => tile !== null))];
        
        tileMarkers1.forEach(tile => {
            const tileElement = this.getTileElementByCoordinate(tile);
            if (tileElement) {
                tileElement.classList.add('valid-move', 'tile-marker-1');
            }
        });
    }
    
    highlightTileMarkers2(matchingMoves) {
        // Get unique tile_marker_2 values from matching moves
        const tileMarkers2 = [...new Set(matchingMoves.map(move => move.tile_marker_2).filter(tile => tile !== null))];
        
        tileMarkers2.forEach(tile => {
            const tileElement = this.getTileElementByCoordinate(tile);
            if (tileElement) {
                tileElement.classList.add('valid-move', 'tile-marker-2');
            }
        });
    }
    
    getTileElementByCoordinate(tileCoordinate) {
        // Convert tile coordinate (e.g., 'A1') to row/col indices
        const col = tileCoordinate.charCodeAt(0) - 65; // A=0, B=1, etc.
        const row = 5 - parseInt(tileCoordinate.charAt(1)); // 1=4, 2=3, etc.
        
        return document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    }
    
    async handleCardMoveTileClick(tileElement) {
        const row = parseInt(tileElement.dataset.row);
        const col = parseInt(tileElement.dataset.col);
        const tileCoordinate = this.coordinatesToTile(row, col);
        
        if (this.currentHighlightState === 'tile_marker_1') {
            // First click - find moves with matching tile_marker_1
            const matchingMoves = this.cardMoves.filter(move => move.tile_marker_1 === tileCoordinate);
            
            if (matchingMoves.length === 0) return;
            
            // Check if we have tile_marker_2 moves
            const hasTileMarker2 = matchingMoves.some(move => move.tile_marker_2 !== null);
            
            if (hasTileMarker2) {
                // Option 1: Show tile_marker_2 highlights
                this.clearHighlights();
                this.currentHighlightState = 'tile_marker_2';
                this.tempMovesList = matchingMoves;
                this.highlightTileMarkers2(matchingMoves);
            } else {
                // Option 2: Play the move directly
                const moveIndex = this.cardMoves.indexOf(matchingMoves[0]);
                await this.playCardMoveByIndex(moveIndex);
            }
        } else if (this.currentHighlightState === 'tile_marker_2') {
            // Second click - find the specific move with matching tile_marker_2
            const matchingMoves = this.tempMovesList.filter(move => move.tile_marker_2 === tileCoordinate);
            
            if (matchingMoves.length === 0) return;
            
            if (matchingMoves.length > 1) {
                console.error('Multiple moves found with same tile_marker_2:', matchingMoves);
                throw new Error('Multiple moves found with same tile_marker_2');
            }
            
            // Play the specific move
            const moveIndex = this.cardMoves.indexOf(matchingMoves[0]);
            await this.playCardMoveByIndex(moveIndex); // TODO
        }
    }
    
    async playCardMoveByIndex(moveIndex) {
        const moveData = {
            type: 'card',
            card_index: this.selectedCard.index,
            move_index: moveIndex
        };

        const success = await this.makeMove(moveData);
        if (success) {
            this.selectedCard = null;
            this.cardMoves = [];
            this.currentHighlightState = null;
            this.tempMovesList = [];
        }
    }

    updateMagicBall() {
        if (!this.gameState || !this.gameState.ball_position) return;

        const magicBall = document.getElementById('magicBall');
        const position = this.gameState.ball_position;
        
        // Update magic ball appearance based on position
        magicBall.className = `magic-ball ${position}`;
        
        // Position the ball vertically based on its position (keep horizontal position on left)
        let topPosition = '0px'; // Default middle position
        
        switch (position) {
            case 'white':
                topPosition = '180px'; // Closer to white side (bottom)
                break;
            case 'black':
                topPosition = '-180px'; // Closer to black side (top)
                break;
            case 'middle':
                topPosition = '0px'; // Middle position
                break;
        }
        
        magicBall.style.top = topPosition;

        // Add visual effect based on ball position
        this.updateBallEffects(position);
    }

    updateBallEffects(position) {
        // Add visual effects based on magic ball position
        const board = document.getElementById('gameBoard');
        
        // Remove previous effects
        board.classList.remove('ball-white', 'ball-black', 'ball-middle');
        
        // Add current effect
        board.classList.add(`ball-${position}`);
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
        // Check if game is over
        if (this.gameState.game_status !== 1) {
            console.log('Game is over, ignoring tile click');
            this.clearHighlights();
            return;
        }
        
        // If it's an AI game and not human's turn, ignore clicks
        if (this.gameType === 'human_vs_ai' && !this.isHumanTurn()) {
            console.log('Not human turn, ignoring click');
            return;
        }
        
        // Check if we're in card move selection mode
        if (this.selectedCard && this.cardMoves.length > 0 && 
            (this.currentHighlightState === 'tile_marker_1' || this.currentHighlightState === 'tile_marker_2')) {
            await this.handleCardMoveTileClick(tileElement);
            return;
        }
        
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
            // Try to move to this tile
            await this.movePawnToTile(row, col);
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
            source_tile: sourceTile,
            target_tile: targetTile
        };

        const success = await this.makeMove(moveData);
        if (success) {
            this.selectedTile = null;
        }
    }

    async playCardMove(row, col) {
        if (!this.selectedCard || this.cardMoves.length === 0) return;

        // For now, use the first available move
        const moveIndex = 0;
        
        const moveData = {
            type: 'card',
            card_index: this.selectedCard.index,
            move_index: moveIndex
        };

        const success = await this.makeMove(moveData);
        if (success) {
            this.selectedCard = null;
            this.cardMoves = [];
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
        document.querySelectorAll('.tile.selected, .tile.valid-move, .tile.tile-marker-1, .tile.tile-marker-2, .card.selected, .pawn.selected').forEach(el => {
            el.classList.remove('selected', 'valid-move', 'tile-marker-1', 'tile-marker-2');
            // Reset card visual effects (but not for used cards)
            if (el.classList.contains('card') && !el.classList.contains('used')) {
                el.style.transform = '';
                el.style.boxShadow = '';
                el.style.border = '';
            }
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
            // Hide turn indicator for AI games
            if (this.gameType === 'human_vs_ai') {
                turnIndicator.style.display = 'none';
            } else {
                turnIndicator.style.display = 'block';
                turnIndicator.textContent = `${currentPlayer.charAt(0).toUpperCase() + currentPlayer.slice(1)}'s Turn`;
                turnIndicator.className = `turn-indicator ${currentPlayer}`;
            }
            
            // Show magic ball position effect
            const ballPosition = this.gameState.ball_position;
            let statusText = '';
            let moveText = '';
            
            if (this.gameType === 'human_vs_ai') {
                if (this.isHumanTurn()) {
                    statusText = 'Your turn';
                    moveText = 'Select a card or make a push move';
                } else {
                    statusText = 'AI is thinking...';
                    moveText = 'Please wait for AI to make its move';
                }
            } else {
                statusText = `Current player: ${currentPlayer}`;
                moveText = 'Select a card or make a push move';
            }
            
            if (ballPosition === 'white' && currentPlayer === 'black') {
                moveText = 'Ball favors White - Black has limited moves';
            } else if (ballPosition === 'black' && currentPlayer === 'white') {
                moveText = 'Ball favors Black - White has limited moves';
            }
            
            gameStatus.textContent = statusText;
            moveInfo.textContent = moveText;
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
            
            turnIndicator.style.display = 'block';
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

// Global function to start a new game
function startNewGame() {
    // Store current game configuration in session storage
    if (window.currentGameBoard && window.currentGameBoard.gameState) {
        sessionStorage.setItem('gameType', window.currentGameBoard.gameType);
        sessionStorage.setItem('playerSide', window.currentGameBoard.humanPlayerSide);
    }
    
    // Clear moves history
    const movesList = document.getElementById('movesList');
    if (movesList) {
        movesList.innerHTML = '';
    }
    
    // Create a new game board instance with the same configuration
    window.currentGameBoard = new GameBoard();
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new GameBoard();
}); 