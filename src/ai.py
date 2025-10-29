import copy
import random
from multiprocessing import Pool, cpu_count
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
    opponent_color = 'white' if color == 'black' else 'black'
    
    # Material and position evaluation
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
    
    # Build attack maps for both colors
    our_attacks = set()
    opponent_attacks = set()
    
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col].piece
            if piece:
                board.calc_moves(piece, row, col, bool=False)
                for move in piece.moves:
                    target = (move.final.row, move.final.col)
                    if piece.color == color:
                        our_attacks.add(target)
                    else:
                        opponent_attacks.add(target)
    
    # Evaluate hanging pieces and threats
    for row in range(8):
        for col in range(8):
            piece = board.squares[row][col].piece
            if piece:
                square = (row, col)
                piece_value = PIECE_VALUES[piece.name.lower()]
                
                if piece.color == color:
                    # Our piece
                    if square in opponent_attacks:
                        if square not in our_attacks:
                            # Hanging piece - major penalty
                            score -= piece_value * 0.9
                        else:
                            # Attacked but defended - smaller penalty based on value
                            score -= piece_value * 0.1
                else:
                    # Opponent's piece
                    if square in our_attacks:
                        if square not in opponent_attacks:
                            # Opponent's hanging piece - bonus
                            score += piece_value * 0.9
    
    # Mobility bonus (lighter weight to avoid slowing down)
    score += len(our_attacks) * 10
    score -= len(opponent_attacks) * 10
    
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
        best_moves = []  # Track all moves with the best score
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
                best_moves = [move]  # New best score, reset list
            elif eval_score == max_eval:
                best_moves.append(move)  # Equal score, add to list
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        # Randomly choose among equally good moves to avoid repetition
        best_move = random.choice(best_moves) if best_moves else None
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

def evaluate_move_parallel(args):
    """
    Helper function for parallel move evaluation.
    Must be at module level for multiprocessing.
    """
    board, move, color, depth = args
    temp_board = copy.deepcopy(board)
    temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
    temp_board.move(temp_piece, move, testing=True)
    eval_score, _ = minimax(temp_board, depth - 1, -float('inf'), float('inf'), False, color)
    return (move, eval_score)

def get_best_move(board, color, depth=2, use_parallel=True):
    """
    Get the best move for the given color using Minimax.
    Uses multiprocessing for parallel evaluation when use_parallel=True.
    """
    moves = get_all_moves(board, color)
    
    if not moves:
        return None
    
    # For small number of moves or depth 1, single-threaded is faster
    if len(moves) <= 4 or depth <= 1 or not use_parallel:
        _, best_move = minimax(board, depth, -float('inf'), float('inf'), True, color)
        return best_move
    
    # Parallel evaluation for root level moves
    # Sort moves: captures first
    moves.sort(key=lambda m: 1 if board.squares[m.final.row][m.final.col].has_piece() else 0, reverse=True)
    
    # Prepare arguments for parallel processing
    args_list = [(board, move, color, depth) for move in moves]
    
    try:
        # Use number of available CPU cores
        num_processes = min(cpu_count(), len(moves))
        with Pool(processes=num_processes) as pool:
            results = pool.map(evaluate_move_parallel, args_list)
        
        # Find best move(s) from results
        best_score = max(results, key=lambda x: x[1])[1]
        best_moves = [move for move, score in results if score == best_score]
        
        # Randomly choose among equally good moves
        return random.choice(best_moves) if best_moves else None
    except Exception as e:
        # Fallback to single-threaded if multiprocessing fails
        print(f"Parallel processing failed: {e}. Using single-threaded mode.")
        _, best_move = minimax(board, depth, -float('inf'), float('inf'), True, color)
        return best_move