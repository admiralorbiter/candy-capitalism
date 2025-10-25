"""
Rendering system for the game world.

Handles world rendering, sprite management, and visual effects
with support for layered rendering and camera systems.
"""

import pygame
from typing import List, Dict, Any, Optional
from ..entities.base_entity import BaseEntity
from ..entities.kid import Kid
from ..entities.house import House
from .camera import Camera
from ..core.constants import COLORS, SCREEN_SIZE


class Renderer:
    """
    Main rendering system for the game world.
    
    Handles rendering of all game entities with support for
    layered rendering and camera systems.
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the renderer.
        
        Args:
            screen: Pygame screen surface to render to
        """
        self.screen = screen
        self.camera = Camera()
        
        # Rendering layers
        self.layers = {
            'background': [],
            'world': [],
            'effects': [],
            'ui': []
        }
        
        # Sprite management
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.font_cache: Dict[tuple, pygame.Font] = {}
        
    def render_world(self, world, dt: float = 0.0):
        """
        Render the entire game world.
        
        Args:
            world: GameWorld instance to render
            dt: Delta time for animations
        """
        # Clear screen
        self.screen.fill(COLORS['BACKGROUND'])
        
        # Render background layer
        self._render_background()
        
        # Render world entities
        self._render_entities(world)
        
        # Render effects layer
        self._render_effects()
        
        # Render UI layer
        self._render_ui()
    
    def _render_background(self):
        """Render background elements."""
        # For now, just a simple grid pattern
        grid_size = 50
        for x in range(0, SCREEN_SIZE[0], grid_size):
            pygame.draw.line(self.screen, COLORS['DARK_GRAY'], 
                           (x, 0), (x, SCREEN_SIZE[1]), 1)
        for y in range(0, SCREEN_SIZE[1], grid_size):
            pygame.draw.line(self.screen, COLORS['DARK_GRAY'], 
                           (0, y), (SCREEN_SIZE[0], y), 1)
    
    def _render_entities(self, world):
        """Render all world entities."""
        # Render houses first (background)
        for house in world.houses:
            if house.active and house.visible:
                self._render_house(house)
        
        # Render kids
        for kid in world.kids:
            if kid.active and kid.visible:
                self._render_kid(kid)
        
        # Render trading blocs (visual indicators)
        for bloc in world.trading_blocs:
            self._render_trading_bloc(bloc, world.kids)
    
    def _render_house(self, house: House):
        """Render a house entity."""
        # Convert world position to screen position
        screen_pos = self.camera.world_to_screen(house.position)
        
        # Draw house as a rectangle
        house_rect = pygame.Rect(
            screen_pos.x - 20, screen_pos.y - 15,
            40, 30
        )
        
        # Choose color based on house state
        if house.is_blessed():
            color = COLORS['GREEN']
        elif house.is_cursed():
            color = COLORS['RED']
        else:
            color = COLORS['GRAY']
        
        pygame.draw.rect(self.screen, color, house_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], house_rect, 2)
        
        # Draw power effect indicators
        if house.is_blessed() or house.is_cursed():
            effect_color = COLORS['YELLOW'] if house.is_blessed() else COLORS['RED']
            pygame.draw.circle(self.screen, effect_color, 
                             screen_pos.to_int_tuple(), 25, 2)
    
    def _render_kid(self, kid: Kid):
        """Render a kid entity."""
        # Convert world position to screen position
        screen_pos = self.camera.world_to_screen(kid.position)
        
        # Draw kid as a colored circle
        color = self._get_kid_color(kid)
        radius = 8
        
        pygame.draw.circle(self.screen, color, screen_pos.to_int_tuple(), radius)
        
        # Draw mood indicator
        self._render_mood_indicator(kid, screen_pos)
        
        # Draw inventory indicator
        self._render_inventory_indicator(kid, screen_pos)
    
    def _get_kid_color(self, kid: Kid) -> tuple:
        """Get color for a kid based on their state."""
        if kid.state.name == "FLEEING":
            return COLORS['RED']
        elif kid.state.name == "IN_TRADE":
            return COLORS['YELLOW']
        elif kid.mood.name == "PANIC":
            return COLORS['ORANGE']
        elif kid.mood.name == "HAPPY":
            return COLORS['GREEN']
        else:
            return COLORS['WHITE']
    
    def _render_mood_indicator(self, kid: Kid, screen_pos):
        """Render mood indicator above kid."""
        mood_symbols = {
            'HAPPY': '😊',
            'NEUTRAL': '😐',
            'ANXIOUS': '😰',
            'GREEDY': '😈',
            'PANIC': '😱'
        }
        
        symbol = mood_symbols.get(kid.mood.name, '?')
        font = self._get_font(16)
        text_surface = font.render(symbol, True, COLORS['WHITE'])
        
        # Position above kid
        text_rect = text_surface.get_rect(center=(screen_pos.x, screen_pos.y - 20))
        self.screen.blit(text_surface, text_rect)
    
    def _render_inventory_indicator(self, kid: Kid, screen_pos):
        """Render small inventory indicator."""
        if not kid.inventory:
            return
        
        # Count total candy
        total_candy = sum(kid.inventory.values())
        if total_candy == 0:
            return
        
        # Draw small indicator
        indicator_rect = pygame.Rect(
            screen_pos.x - 12, screen_pos.y + 12,
            24, 4
        )
        
        # Color based on total candy value
        if total_candy > 10:
            color = COLORS['GREEN']
        elif total_candy > 5:
            color = COLORS['YELLOW']
        else:
            color = COLORS['RED']
        
        pygame.draw.rect(self.screen, color, indicator_rect)
    
    def _render_trading_bloc(self, bloc, kids: List[Kid]):
        """Render trading bloc visual indicators."""
        if not bloc.members:
            return
        
        # Get member positions
        member_positions = []
        for kid_id in bloc.members:
            kid = next((k for k in kids if k.id == kid_id), None)
            if kid and kid.active:
                member_positions.append(kid.position)
        
        if len(member_positions) < 2:
            return
        
        # Draw connections between members
        for i, pos1 in enumerate(member_positions):
            for pos2 in member_positions[i+1:]:
                screen_pos1 = self.camera.world_to_screen(pos1)
                screen_pos2 = self.camera.world_to_screen(pos2)
                
                pygame.draw.line(self.screen, bloc.color, 
                               screen_pos1.to_int_tuple(), 
                               screen_pos2.to_int_tuple(), 2)
    
    def _render_effects(self):
        """Render visual effects."""
        # Placeholder for particle effects, etc.
        pass
    
    def _render_ui(self):
        """Render UI elements."""
        # Placeholder for UI rendering
        pass
    
    def _get_font(self, size: int) -> pygame.Font:
        """Get cached font."""
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]
    
    def set_camera(self, camera: Camera):
        """Set the camera for rendering."""
        self.camera = camera
    
    def get_camera(self) -> Camera:
        """Get the current camera."""
        return self.camera
    
    def clear_cache(self):
        """Clear sprite and font caches."""
        self.sprite_cache.clear()
        self.font_cache.clear()
