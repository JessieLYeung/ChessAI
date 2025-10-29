import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.state = 'menu'  # Add state for menu or game
        self.ai_timer = 0  # Timer for AI delay
        self.pvp_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        self.ai_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    def show_menu(self, surface):
        surface.fill((0, 0, 0))  # Black background
        font = pygame.font.SysFont('monospace', 36, bold=True)
        title = font.render('ChessBot', True, (255, 255, 255))
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Draw PvP button
        pygame.draw.rect(surface, (255, 255, 255), self.pvp_button)
        pvp_text = font.render('PvP', True, (0, 0, 0))
        surface.blit(pvp_text, (self.pvp_button.centerx - pvp_text.get_width() // 2, self.pvp_button.centery - pvp_text.get_height() // 2))
        
        # Draw AI button
        pygame.draw.rect(surface, (255, 255, 255), self.ai_button)
        ai_text = font.render('AI Mode', True, (0, 0, 0))
        surface.blit(ai_text, (self.ai_button.centerx - ai_text.get_width() // 2, self.ai_button.centery - ai_text.get_height() // 2))

    def show_game_over(self, surface):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont('monospace', 48, bold=True)
        small_font = pygame.font.SysFont('monospace', 24)
        
        if self.game.winner == 'draw':
            text = font.render('STALEMATE', True, (255, 255, 255))
            subtext = small_font.render('It\'s a draw!', True, (200, 200, 200))
        else:
            winner_text = f'{self.game.winner.upper()} WINS!'
            text = font.render(winner_text, True, (255, 255, 255))
            subtext = small_font.render('Checkmate!', True, (200, 200, 200))
        
        # Center the text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        
        surface.blit(text, text_rect)
        surface.blit(subtext, subtext_rect)
        
        # Show restart instruction
        restart_font = pygame.font.SysFont('monospace', 18)
        restart_text = restart_font.render('Press R to restart or ESC for menu', True, (150, 150, 150))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        surface.blit(restart_text, restart_rect)

    def mainloop(self):
        
        screen = self.screen

        while True:
            # Always reference current game state
            game = self.game
            board = self.game.board
            dragger = self.game.dragger
            
            if self.state == 'menu':
                self.show_menu(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if self.pvp_button.collidepoint(pos):
                            game.ai_mode = False
                            self.state = 'game'
                        elif self.ai_button.collidepoint(pos):
                            game.ai_mode = True
                            self.state = 'game'
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            game.ai_mode = False
                            self.state = 'game'
                        elif event.key == pygame.K_a:
                            game.ai_mode = True
                            self.state = 'game'
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                # show methods
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                # Show game over message if game is over
                if game.game_over:
                    self.show_game_over(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                    
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)                            

                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()
                                if game.ai_mode:
                                    self.ai_timer = pygame.time.get_ticks() + 500  # 0.5 second delay
                        
                        dragger.undrag_piece()
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        
                        # Handle game over state first
                        if game.game_over:
                            # restart game
                            if event.key == pygame.K_r:
                                game.reset()
                                # Check if AI should move first after reset
                                if game.ai_mode and game.next_player == 'black':
                                    self.ai_timer = pygame.time.get_ticks() + 500
                                else:
                                    self.ai_timer = 0
                            # back to menu
                            elif event.key == pygame.K_ESCAPE:
                                self.state = 'menu'
                                game.reset()
                                self.ai_timer = 0
                        else:
                            # Normal game controls when game is not over
                            # changing themes
                            if event.key == pygame.K_t:
                                game.change_theme()

                            # toggle AI mode
                            if event.key == pygame.K_a:
                                game.toggle_ai_mode()

                            # restart game
                            if event.key == pygame.K_r:
                                game.reset()
                                # Check if AI should move first after reset
                                if game.ai_mode and game.next_player == 'black':
                                    self.ai_timer = pygame.time.get_ticks() + 500
                                else:
                                    self.ai_timer = 0
                            
                            # back to menu
                            if event.key == pygame.K_ESCAPE:
                                self.state = 'menu'
                                game.reset()
                                self.ai_timer = 0

                    # quit application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            # AI move execution (check outside event loop)
            if self.ai_timer > 0 and pygame.time.get_ticks() > self.ai_timer and not game.game_over:
                self.ai_timer = 0
                game.make_ai_move()
            
            pygame.display.set_caption(f'Chess - AI Mode: {"ON" if game.ai_mode else "OFF"}')
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
