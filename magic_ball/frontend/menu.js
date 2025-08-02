function startNewGame() {
    // Store game type in session storage
    sessionStorage.setItem('gameType', 'human_vs_human');
    sessionStorage.removeItem('playerSide');
    
    // Navigate to game page
    window.location.href = 'game.html';
}

function showAIOptions() {
    document.getElementById('aiOptions').style.display = 'block';
}

function hideAIOptions() {
    document.getElementById('aiOptions').style.display = 'none';
}

function startAIGame() {
    const playerSide = document.querySelector('input[name="playerSide"]:checked').value;
    
    // Store game type and player side in session storage
    sessionStorage.setItem('gameType', 'human_vs_ai');
    sessionStorage.setItem('playerSide', playerSide);
    
    // Navigate to game page
    window.location.href = 'game.html';
} 