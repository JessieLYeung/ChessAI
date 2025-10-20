// Chessboard.js integration

let board = null;
const game = new Chess(); // Using chess.js for FEN and validation

function onDragStart(source, piece, position, orientation) {
    // Check if it's the correct player's turn
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false;
    }
}

function onDrop(source, target) {
    const move = game.move({
        from: source,
        to: target,
        promotion: 'q' // Always promote to queen for simplicity
    });

    if (move === null) return 'snapback';

    // If AI mode and it's black's turn, make AI move
    if (aiMode && game.turn() === 'b') {
        setTimeout(makeAIMove, 1000);
    }
}

function makeAIMove() {
    const bestMove = getBestMove(game);
    if (bestMove) {
        game.move(bestMove);
        board.position(game.fen());
    }
}

function getBestMove(game) {
    const moves = game.moves({verbose: true});
    let bestMove = null;
    let bestValue = -Infinity;

    for (const move of moves) {
        game.move(move);
        const value = -minimax(game, 2, -Infinity, Infinity, false);
        game.undo();

        if (value > bestValue) {
            bestValue = value;
            bestMove = move;
        }
    }
    return bestMove;
}

function minimax(game, depth, alpha, beta, maximizing) {
    if (depth === 0) {
        return evaluatePosition(game);
    }

    const moves = game.moves();

    if (maximizing) {
        let maxEval = -Infinity;
        for (const move of moves) {
            game.move(move);
            const evaluation = minimax(game, depth - 1, alpha, beta, false);
            game.undo();
            maxEval = Math.max(maxEval, evaluation);
            alpha = Math.max(alpha, evaluation);
            if (beta <= alpha) break;
        }
        return maxEval;
    } else {
        let minEval = Infinity;
        for (const move of moves) {
            game.move(move);
            const evaluation = minimax(game, depth - 1, alpha, beta, true);
            game.undo();
            minEval = Math.min(minEval, evaluation);
            beta = Math.min(beta, evaluation);
            if (beta <= alpha) break;
        }
        return minEval;
    }
}

function evaluatePosition(game) {
    const pieceValues = {
        'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 900
    };

    let evaluation = 0;
    const board = game.board();

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (piece) {
                const value = pieceValues[piece.type];
                evaluation += piece.color === 'w' ? value : -value;
            }
        }
    }
    return evaluation;
}

const config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop
};

board = Chessboard('board', config);

let aiMode = false;

document.getElementById('pvpBtn').addEventListener('click', () => {
    aiMode = false;
    game.reset();
    board.start();
    document.getElementById('status').textContent = 'Player vs Player mode';
});

document.getElementById('aiBtn').addEventListener('click', () => {
    aiMode = true;
    game.reset();
    board.start();
    document.getElementById('status').textContent = 'Player vs AI mode';
});

document.getElementById('resetBtn').addEventListener('click', () => {
    game.reset();
    board.start();
    document.getElementById('status').textContent = 'Game reset';
});