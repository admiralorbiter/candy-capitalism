"""
Main game class and game loop.

Handles initialization, main game loop, and coordination between systems.
"""

import pygame
from typing import Optional

from .constants import SCREEN_SIZE, FPS_TARGET, COLORS
from .game_state import GameState, GameStateMachine, BaseState
from .config_manager import config_manager


class Game:
    """
    Main game class that manages the game loop and coordinates all systems.
    
    Based on the architecture from systems.md with a focus on clean separation
    of concerns and event-driven design.
    """
    
    def __init__(self):
        """Initialize the game and all its systems."""
        pygame.init()
        
        # Create game window
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Candy Capitalism")
        
        # Game clock for FPS control
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load configurations
        config_manager.load_all()
        
        # Initialize core systems
        self.state_machine = GameStateMachine()
        self._setup_states()
        
        # Game state
        self.delta_time = 0.0
        self.game_time = 0.0
        
        print("Candy Capitalism initialized successfully")
    
    def _setup_states(self):
        """Set up all game states."""
        # For now, just register placeholder states
        # These will be implemented in later sprints
        self.state_machine.register_state(GameState.MAIN_MENU, MainMenuState())
        self.state_machine.register_state(GameState.PLAYING, PlayingState())
        self.state_machine.register_state(GameState.PAUSED, PausedState())
    
    def run(self):
        """Main game loop."""
        print("Starting game loop...")
        
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS_TARGET) / 1000.0
            self.delta_time = min(dt, 0.1)  # Cap to prevent spiral of death
            self.game_time += self.delta_time
            
            # Handle events
            self._handle_events()
            
            # Update game state
            self.state_machine.update(self.delta_time)
            
            # Render
            self._render()
            
            # Update display
            pygame.display.flip()
        
        self._cleanup()
    
    def _handle_events(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    # Pass to current state
                    self.state_machine.handle_event(event)
            else:
                # Pass to current state
                self.state_machine.handle_event(event)
    
    def _render(self):
        """Render the current frame."""
        # Clear screen
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Let current state handle rendering
        if hasattr(self.state_machine.states.get(self.state_machine.current_state), 'render'):
            self.state_machine.states[self.state_machine.current_state].render(self.screen)
    
    def _cleanup(self):
        """Clean up resources before exiting."""
        pygame.quit()
        print("Game cleanup complete")


class MainMenuState(BaseState):
    """Main menu state (placeholder for now)."""
    
    def on_enter(self, data=None):
        print("Entered main menu")
    
    def render(self, screen):
        # Simple placeholder rendering
        font = pygame.font.Font(None, 48)
        text = font.render("Candy Capitalism", True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
        screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 24)
        instructions = font_small.render("Press ESC to quit", True, COLORS['GRAY'])
        inst_rect = instructions.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 + 50))
        screen.blit(instructions, inst_rect)


class PlayingState(BaseState):
    """Playing state (placeholder for now)."""
    
    def on_enter(self, data=None):
        print("Entered playing state")
    
    def render(self, screen):
        # Simple placeholder rendering
        font = pygame.font.Font(None, 36)
        text = font.render("Playing State - Coming Soon!", True, COLORS['GREEN'])
        text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
        screen.blit(text, text_rect)


class PausedState(BaseState):
    """Paused state (placeholder for now)."""
    
    def on_enter(self, data=None):
        print("Entered paused state")
    
    def render(self, screen):
        # Simple placeholder rendering
        font = pygame.font.Font(None, 36)
        text = font.render("Paused", True, COLORS['YELLOW'])
        text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
        screen.blit(text, text_rect)
