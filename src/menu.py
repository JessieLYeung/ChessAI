"""
Main menu system for the chess game
"""

import pygame
import sys
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, PLAYER_WHITE, PLAYER_BLACK

class MainMenu:
    """Main menu for selecting game mode"""
    
    def __init__(self):
        """Initialize the main menu"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Chess Bot - Main Menu")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Menu state
        self.selected_option = 0
        self.in_ai_options = False
        self.ai_color = PLAYER_BLACK
        self.ai_difficulty = 3
        
        # Button rectangles
        self.buttons = []
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Set up button rectangles"""
        button_width = 300
        button_height = 60
        start_y = 250
        spacing = 80
        
        self.buttons = [
            pygame.Rect((WINDOW_WIDTH - button_width) // 2, start_y, button_width, button_height),
            pygame.Rect((WINDOW_WIDTH - button_width) // 2, start_y + spacing, button_width, button_height),
            pygame.Rect((WINDOW_WIDTH - button_width) // 2, start_y + spacing * 2, button_width, button_height)
        ]
    
    def run(self):
        """Run the main menu loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.in_ai_options:
                            self.in_ai_options = False
                        else:
                            return None
                    
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % 3
                    
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 3
                    
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        result = self._handle_selection()
                        if result:
                            return result
                    
                    # AI options controls
                    elif self.in_ai_options:
                        if event.key == pygame.K_LEFT:
                            if self.selected_option == 0:  # Color selection
                                self.ai_color = PLAYER_WHITE if self.ai_color == PLAYER_BLACK else PLAYER_BLACK
                            elif self.selected_option == 1:  # Difficulty
                                self.ai_difficulty = max(1, self.ai_difficulty - 1)
                        
                        elif event.key == pygame.K_RIGHT:
                            if self.selected_option == 0:  # Color selection
                                self.ai_color = PLAYER_WHITE if self.ai_color == PLAYER_BLACK else PLAYER_BLACK
                            elif self.selected_option == 1:  # Difficulty
                                self.ai_difficulty = min(5, self.ai_difficulty + 1)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self._handle_mouse_click(event.pos)
                
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_mouse_hover(event.pos)
            
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        return None
    
    def _handle_selection(self):
        """Handle menu selection"""
        if not self.in_ai_options:
            if self.selected_option == 0:  # Player vs Player
                return {'mode': 'pvp'}
            elif self.selected_option == 1:  # Player vs AI
                self.in_ai_options = True
                self.selected_option = 0
            elif self.selected_option == 2:  # Quit
                return None
        else:
            if self.selected_option == 2:  # Start AI game
                return {
                    'mode': 'ai',
                    'ai_color': self.ai_color,
                    'difficulty': self.ai_difficulty
                }
        
        return False
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        if not self.in_ai_options:
            for i, button in enumerate(self.buttons):
                if button.collidepoint(pos):
                    self.selected_option = i
                    result = self._handle_selection()
                    if result:
                        return result
        else:
            # AI options clicks
            for i, button in enumerate(self.buttons):
                if button.collidepoint(pos):
                    if i == 0:  # Color selection
                        self.ai_color = PLAYER_WHITE if self.ai_color == PLAYER_BLACK else PLAYER_BLACK
                    elif i == 1:  # Difficulty (cycle through)
                        self.ai_difficulty = (self.ai_difficulty % 5) + 1
                    elif i == 2:  # Start game
                        return {
                            'mode': 'ai',
                            'ai_color': self.ai_color,
                            'difficulty': self.ai_difficulty
                        }
    
    def _handle_mouse_hover(self, pos):
        """Handle mouse hover for button highlighting"""
        for i, button in enumerate(self.buttons):
            if button.collidepoint(pos):
                self.selected_option = i
                break
    
    def _draw(self):
        """Draw the menu"""
        self.screen.fill(WHITE)
        
        if not self.in_ai_options:
            self._draw_main_menu()
        else:
            self._draw_ai_options()
    
    def _draw_main_menu(self):
        """Draw the main menu"""
        # Title
        title_text = self.title_font.render("AI Chess Bot", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Menu options
        options = ["Player vs Player", "Player vs AI", "Quit"]
        
        for i, (option, button) in enumerate(zip(options, self.buttons)):
            # Button background
            color = (200, 200, 200) if i == self.selected_option else (240, 240, 240)
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, BLACK, button, 3)
            
            # Button text
            text = self.button_font.render(option, True, BLACK)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)
        
        # Instructions
        instruction_text = self.small_font.render("Use arrow keys and Enter, or click to select", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, 520))
        self.screen.blit(instruction_text, instruction_rect)
    
    def _draw_ai_options(self):
        """Draw AI game options"""
        # Title
        title_text = self.title_font.render("AI Game Options", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Options
        options = [
            f"Your Color: {self.ai_color.title()} (AI plays {PLAYER_BLACK if self.ai_color == PLAYER_WHITE else PLAYER_WHITE})",
            f"AI Difficulty: {self.ai_difficulty}/5",
            "Start Game"
        ]
        
        for i, (option, button) in enumerate(zip(options, self.buttons)):
            # Button background
            color = (200, 200, 200) if i == self.selected_option else (240, 240, 240)
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, BLACK, button, 3)
            
            # Button text
            font = self.small_font if i < 2 else self.button_font
            text = font.render(option, True, BLACK)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)
        
        # Instructions
        instructions = [
            "Use arrow keys to navigate",
            "Left/Right to change values",
            "Enter to start game",
            "ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 480 + i * 25))
            self.screen.blit(text, text_rect)
        
        # Difficulty description
        difficulty_descriptions = {
            1: "Very Easy - Quick moves",
            2: "Easy - Basic strategy",
            3: "Medium - Good planning",
            4: "Hard - Strong tactics",
            5: "Very Hard - Deep thinking"
        }
        
        desc_text = self.small_font.render(difficulty_descriptions[self.ai_difficulty], True, (100, 100, 100))
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, 430))
        self.screen.blit(desc_text, desc_rect)