import copy
from board import Board
from move import Move
from square import Square
from piece import *

# Piece values for evaluation
PIECE_VALUES = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000
}

# Piece-square tables (for white, flip for black)
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

PIECE_TABLES = {
    'pawn': PAWN_TABLE,
    'knight': KNIGHT_TABLE,
    'bishop': BISHOP_TABLE,
    'rook': ROOK_TABLE,
    'queen': QUEEN_TABLE,
    'king': KING_TABLE
}

def evaluate_board(board, color):
    """
    Evaluate the board position for the given color.
    Positive score means advantage for the color.
    """
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col].piece
            if piece:
                value = PIECE_VALUES[piece.name.lower()]
                table = PIECE_TABLES[piece.name.lower()]
                if piece.color == 'white':
                    pos_value = table[row][col]
                else:
                    pos_value = table[7 - row][col]  # Flip for black
                total_value = value + pos_value
                if piece.color == color:
                    score += total_value
                else:
                    score -= total_value
    return score

def get_all_moves(board, color):
    """
    Get all legal moves for the given color.
    """
    moves = []
    for row in range(8):
        for col in range(8):
            if board.squares[row][col].has_piece() and board.squares[row][col].piece.color == color:
                piece = board.squares[row][col].piece
                board.calc_moves(piece, row, col, bool=True)
                moves.extend(piece.moves)
    return moves

def minimax(board, depth, alpha, beta, maximizing_player, color):
    """
    Minimax algorithm with alpha-beta pruning and quiescence.
    """
    if depth == 0:
        return quiescence(board, alpha, beta, color), None

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        moves = get_all_moves(board, color)
        # Sort moves: captures first (simple heuristic)
        moves.sort(key=lambda m: 1 if board.squares[m.final.row][m.final.col].has_piece() else 0, reverse=True)
        for move in moves:
            # Make a copy of the board
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
            temp_board.move(temp_piece, move, testing=True)
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False, color)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        opponent_color = 'white' if color == 'black' else 'black'
        moves = get_all_moves(board, opponent_color)
        moves.sort(key=lambda m: 1 if board.squares[m.final.row][m.final.col].has_piece() else 0, reverse=True)
        for move in moves:
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
            temp_board.move(temp_piece, move, testing=True)
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True, color)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, None

def quiescence(board, alpha, beta, color):
    """
    Quiescence search: evaluate until no captures or checks.
    """
    stand_pat = evaluate_board(board, color)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    moves = get_all_moves(board, color)
    # Only consider captures
    capture_moves = [m for m in moves if board.squares[m.final.row][m.final.col].has_piece()]
    for move in capture_moves:
        temp_board = copy.deepcopy(board)
        temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
        temp_board.move(temp_piece, move, testing=True)
        score = -quiescence(temp_board, -beta, -alpha, 'white' if color == 'black' else 'black')
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def get_best_move(board, color, depth=4):
    """
    Get the best move for the given color using Minimax.
    """
    _, best_move = minimax(board, depth, -float('inf'), float('inf'), True, color)
    return best_move