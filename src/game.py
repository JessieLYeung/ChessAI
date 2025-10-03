"""
Main game class that handles the game loop and coordination
"""

import pygame
import sys
from .board import ChessBoard
from .gui import ChessGUI
from .ai import ChessAI
from .utils import GameStats, MoveNotationConverter
from .image_generator import PieceImageGenerator
from .constants import PLAYER_WHITE, PLAYER_BLACK, AI_THINKING_TIME

class ChessGame:
    """Main chess game class"""
    
    def __init__(self, game_mode):
        """
        Initialize the chess game
        
        Args:
            game_mode (dict): Game configuration with mode and difficulty
        """
        # Generate piece images first, before creating GUI
        try:
            PieceImageGenerator.generate_piece_images()
        except Exception as e:
            print(f"Could not generate piece images: {e}")
        
        self.board = ChessBoard()
        self.gui = ChessGUI()
        self.game_mode = game_mode
        self.ai_player = None
        self.ai_thinking = False
        self.ai_start_time = 0
        self.pending_promotion = None
        self.stats = GameStats()
        
        # Initialize AI if needed
        if game_mode['mode'] == 'ai':
            ai_color = game_mode.get('ai_color', PLAYER_BLACK)
            ai_difficulty = game_mode.get('difficulty', 3)
            self.ai_player = ChessAI(ai_color, ai_difficulty)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Record game stats if game finished
                        if self.board.game_over:
                            self.stats.record_game(
                                self.game_mode['mode'], 
                                self.board.winner, 
                                len(self.board.move_history)
                            )
                        running = False
                    elif event.key == pygame.K_r and self.board.game_over:
                        # Record game stats before restart
                        self.stats.record_game(
                            self.game_mode['mode'], 
                            self.board.winner, 
                            len(self.board.move_history)
                        )
                        # Restart game
                        self._restart_game()
                    elif event.key == pygame.K_s:
                        # Save game (disabled during AI thinking)
                        if not self.ai_thinking:
                            self._save_game()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self._handle_mouse_click(event.pos)
            
            # Handle AI moves
            if (self.ai_player and 
                self.board.current_player == self.ai_player.color and 
                not self.board.game_over and 
                not self.ai_thinking and
                not self.pending_promotion):
                
                self._start_ai_thinking()
            
            # Check if AI thinking time is done
            if self.ai_thinking:
                current_time = pygame.time.get_ticks()
                if current_time - self.ai_start_time >= AI_THINKING_TIME:
                    self._execute_ai_move()
            
            # Draw everything
            self.gui.draw_board(self.board)
            
            # Show AI thinking indicator
            if self.ai_thinking:
                self._draw_ai_thinking()
            
            # Show game over screen
            if self.board.game_over:
                self._draw_game_over()
            
            self.gui.update_display()
        
        return False  # Don't restart
    
    def _handle_mouse_click(self, mouse_pos):
        """Handle mouse click events"""
        # Handle promotion dialog clicks
        if self.pending_promotion:
            promotion_piece = self.gui.handle_promotion_click(mouse_pos, self.pending_promotion)
            if promotion_piece:
                from_row, from_col, to_row, to_col = self.pending_promotion[1:]
                if self.board.move_piece(from_row, from_col, to_row, to_col, promotion_piece):
                    self.gui.last_move = ((from_row, from_col), (to_row, to_col))
                    self.gui.clear_selection()
                self.pending_promotion = None
            return
        
        # Don't allow moves during AI thinking or if game is over
        if self.ai_thinking or self.board.game_over:
            return
        
        # Don't allow human moves during AI turn
        if (self.ai_player and 
            self.board.current_player == self.ai_player.color):
            return
        
        # Get square from mouse position
        square = self.gui.get_square_from_mouse(mouse_pos)
        if square:
            result = self.gui.handle_square_click(square, self.board)
            
            if result and result[0] == 'promote':
                self.pending_promotion = result
    
    def _start_ai_thinking(self):
        """Start AI thinking process"""
        self.ai_thinking = True
        self.ai_start_time = pygame.time.get_ticks()
        self.gui.clear_selection()
    
    def _execute_ai_move(self):
        """Execute the AI's chosen move"""
        self.ai_thinking = False
        
        best_move = self.ai_player.get_best_move(self.board)
        
        if best_move:
            from_pos, to_pos = best_move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Check for pawn promotion
            piece = self.board.get_piece(from_row, from_col)
            if (piece and piece.__class__.__name__ == 'Pawn' and
                ((piece.color == PLAYER_WHITE and to_row == 0) or 
                 (piece.color == PLAYER_BLACK and to_row == 7))):
                
                # AI always promotes to Queen
                from .pieces import Queen
                if self.board.move_piece(from_row, from_col, to_row, to_col, Queen):
                    self.gui.last_move = (from_pos, to_pos)
            else:
                # Regular move
                if self.board.move_piece(from_row, from_col, to_row, to_col):
                    self.gui.last_move = (from_pos, to_pos)
    
    def _draw_ai_thinking(self):
        """Draw AI thinking indicator"""
        thinking_text = "AI is thinking..."
        font = pygame.font.Font(None, 36)
        text = font.render(thinking_text, True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 50))
        self.gui.screen.blit(text, text_rect)
    
    def _draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.gui.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        if self.board.winner:
            text = f"{self.board.winner.title()} Wins!"
            color = (255, 255, 0)
        else:
            text = "Draw!"
            color = (255, 255, 255)
        
        game_over_text = font.render(text, True, color)
        text_rect = game_over_text.get_rect(center=(400, 250))
        self.gui.screen.blit(game_over_text, text_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 36)
        restart_text = instruction_font.render("Press R to restart or ESC to exit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(400, 350))
        self.gui.screen.blit(restart_text, restart_rect)
    
    def _restart_game(self):
        """Restart the game"""
        self.board = ChessBoard()
        self.gui.clear_selection()
        self.gui.last_move = None
        self.ai_thinking = False
        self.pending_promotion = None
        
        # Reinitialize AI if needed
        if self.game_mode['mode'] == 'ai':
            ai_color = self.game_mode.get('ai_color', PLAYER_BLACK)
            ai_difficulty = self.game_mode.get('difficulty', 3)
            self.ai_player = ChessAI(ai_color, ai_difficulty)
    
    def _save_game(self):
        """Save the current game state"""
        from .utils import GameSaver
        success = GameSaver.save_game(self.board)
        if success:
            print("Game saved successfully!")
        else:
            print("Failed to save game.")