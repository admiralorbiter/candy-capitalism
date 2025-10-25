"""
Main game class and game loop.

Handles initialization, main game loop, and coordination between systems.
"""

import pygame
from typing import Optional

from .constants import SCREEN_SIZE, FPS_TARGET, COLORS
from .game_state import GameState, GameStateMachine, BaseState
from .config_manager import config_manager
from ..systems.game_world import GameWorld
from ..rendering.renderer import Renderer
from ..rendering.particle_system import ParticleSystem
from ..rendering.floating_text import FloatingTextSystem
from ..ui.market_ticker import MarketTicker
from ..ui.economy_debug import EconomyDebugOverlay
from ..utils.vector2 import Vector2


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
                    if self.state_machine.current_state == GameState.PLAYING:
                        # Pause the game
                        self.state_machine.transition(GameState.PAUSED)
                    else:
                        self.running = False
                else:
                    # Pass to current state
                    result = self.state_machine.handle_event(event)
                    if result == "start_game":
                        self.state_machine.transition(GameState.PLAYING)
                    elif result == "quit":
                        self.running = False
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
    """Main menu state with game start option."""
    
    def on_enter(self, data=None):
        print("Entered main menu")
    
    def handle_event(self, event):
        """Handle input events for main menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start the game
                return "start_game"
            elif event.key == pygame.K_ESCAPE:
                # Quit
                return "quit"
        return False
    
    def render(self, screen):
        # Simple placeholder rendering
        font = pygame.font.Font(None, 48)
        text = font.render("Candy Capitalism", True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
        screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 24)
        instructions = font_small.render("Press SPACE to start, ESC to quit", True, COLORS['GRAY'])
        inst_rect = instructions.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 + 50))
        screen.blit(instructions, inst_rect)


class PlayingState(BaseState):
    """Playing state with world and rendering."""
    
    def __init__(self):
        self.world = GameWorld()
        self.renderer = None
        self.initialized = False
        
        # UI elements
        self.particle_system = ParticleSystem()
        self.floating_text_system = FloatingTextSystem()
        self.market_ticker = MarketTicker(SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.economy_debug = EconomyDebugOverlay(SCREEN_SIZE[0], SCREEN_SIZE[1])
    
    def on_enter(self, data=None):
        print("Entered playing state")
        if not self.initialized:
            self.renderer = Renderer(pygame.display.get_surface())
            
            # Add UI systems to renderer for trade effects
            self.renderer.particle_system = self.particle_system
            self.renderer.floating_text_system = self.floating_text_system
            
            # Generate the map
            self.world.generate_map("default")
            # Spawn kids
            self.world.spawn_kids(10)
            self.initialized = True
            print("Playing state initialized with map and kids")
    
    def update(self, dt):
        """Update the playing state."""
        if self.world:
            self.world.update(dt, self.renderer)
            
            # Update UI elements
            self.particle_system.update(dt)
            self.floating_text_system.update(dt)
            self.market_ticker.update(dt, self.world.economy)
    
    def handle_event(self, event):
        """Handle input events for playing state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                # Toggle debug overlay
                if self.renderer:
                    self.renderer.toggle_debug()
                return True
            elif event.key == pygame.K_h:
                # Toggle help overlay
                if self.renderer:
                    self.renderer.toggle_help()
                return True
            elif event.key == pygame.K_i:
                # Toggle inventory display
                if self.renderer:
                    self.renderer.toggle_inventory_display(self.world)
                return True
            elif event.key == pygame.K_e:
                # Toggle economy debug overlay
                self.economy_debug.toggle()
                return True
            
            # Camera movement (panning)
            elif event.key == pygame.K_LEFT:
                if self.renderer:
                    current_pos = self.renderer.camera.position
                    new_pos = current_pos + Vector2(-100, 0)
                    self.renderer.camera.set_position(new_pos, smooth=False)
                    print(f"Camera moved LEFT to: {new_pos}")
                return True
            elif event.key == pygame.K_RIGHT:
                if self.renderer:
                    current_pos = self.renderer.camera.position
                    new_pos = current_pos + Vector2(100, 0)
                    self.renderer.camera.set_position(new_pos, smooth=False)
                    print(f"Camera moved RIGHT to: {new_pos}")
                return True
            elif event.key == pygame.K_UP:
                if self.renderer:
                    current_pos = self.renderer.camera.position
                    new_pos = current_pos + Vector2(0, -100)
                    self.renderer.camera.set_position(new_pos, smooth=False)
                    print(f"Camera moved UP to: {new_pos}")
                return True
            elif event.key == pygame.K_DOWN:
                if self.renderer:
                    current_pos = self.renderer.camera.position
                    new_pos = current_pos + Vector2(0, 100)
                    self.renderer.camera.set_position(new_pos, smooth=False)
                    print(f"Camera moved DOWN to: {new_pos}")
                return True
            
            # Camera zoom
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                if self.renderer:
                    self.renderer.camera.zoom_in(1.2)
                    print(f"Camera zoomed IN to: {self.renderer.camera.zoom}")
                return True
            elif event.key == pygame.K_MINUS:
                if self.renderer:
                    self.renderer.camera.zoom_out(1.2)
                    print(f"Camera zoomed OUT to: {self.renderer.camera.zoom}")
                return True
            
            # Reset camera to center
            elif event.key == pygame.K_r:
                if self.renderer:
                    self.renderer.camera.set_position(Vector2(1000, 1000), smooth=False)  # Center of world
                    self.renderer.camera.set_zoom(0.5, smooth=False)  # Zoomed out to see more
                    print("Camera reset to center of world")
                return True
        
        # Mouse wheel zoom
        elif event.type == pygame.MOUSEWHEEL:
            if self.renderer:
                if event.y > 0:  # Scroll up - zoom in
                    self.renderer.camera.zoom_in(1.1)
                    print(f"Mouse wheel ZOOM IN to: {self.renderer.camera.zoom}")
                else:  # Scroll down - zoom out
                    self.renderer.camera.zoom_out(1.1)
                    print(f"Mouse wheel ZOOM OUT to: {self.renderer.camera.zoom}")
            return True
        
        return False
    
    def render(self, screen):
        """Render the playing state."""
        if self.world and self.renderer:
            self.renderer.render_world(self.world)
            
            # Render UI elements
            self.particle_system.render(screen, self.renderer.camera)
            self.floating_text_system.render(screen, self.renderer.camera)
            self.market_ticker.render(screen)
            
            # Render debug overlay
            self.economy_debug.render(screen, self.world.economy, self.world.kids, self.renderer.camera)
        else:
            # Fallback rendering
            font = pygame.font.Font(None, 36)
            text = font.render("Playing State - Initializing...", True, COLORS['GREEN'])
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
