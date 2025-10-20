import copy
from board import Board
from move import Move
from square import Square
from piece import *

# Piece values for evaluation
PIECE_VALUES = {
    'pawn': 10,
    'knight': 30,
    'bishop': 30,
    'rook': 50,
    'queen': 90,
    'king': 900
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
                if piece.color == color:
                    score += value
                else:
                    score -= value
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
    Minimax algorithm with alpha-beta pruning.
    """
    if depth == 0:
        return evaluate_board(board, color), None

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        moves = get_all_moves(board, color)
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
        moves = get_all_moves(board, 'white' if color == 'black' else 'black')
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

def get_best_move(board, color, depth=3):
    """
    Get the best move for the given color using Minimax.
    """
    _, best_move = minimax(board, depth, -float('inf'), float('inf'), True, color)
    return best_move