"""
Kid entity class.

Represents a trick-or-treating child with AI behavior, trading capabilities,
and various personality traits that affect their behavior.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from ..utils.vector2 import Vector2
from .base_entity import BaseEntity


class KidState(Enum):
    """Possible states for a kid."""
    IDLE = 0
    MOVING_TO_HOUSE = 1
    TRICK_OR_TREATING = 2
    SEEKING_TRADE = 3
    IN_TRADE = 4
    FLEEING = 5


class PersonalityType(Enum):
    """Kid personality types that affect trading behavior."""
    VALUE_INVESTOR = 0
    MOMENTUM_TRADER = 1
    HOARDER = 2
    SOCIAL_TRADER = 3
    PANIC_SELLER = 4


class Mood(Enum):
    """Kid mood states that affect behavior."""
    HAPPY = 0
    NEUTRAL = 1
    ANXIOUS = 2
    GREEDY = 3
    PANIC = 4


class Kid(BaseEntity):
    """
    Represents a trick-or-treating child with AI behavior.
    
    Each kid has personality traits, preferences, and goals that affect
    their trading behavior and movement patterns.
    """
    
    def __init__(self, kid_id: str, position: Vector2 = None):
        """
        Initialize a kid entity.
        
        Args:
            kid_id: Unique identifier for this kid
            position: Initial position
        """
        super().__init__(kid_id, position)
        
        # AI state
        self.state = KidState.IDLE
        self.personality = PersonalityType.VALUE_INVESTOR
        self.mood = Mood.NEUTRAL
        
        # Trading attributes
        self.preferences: Dict[str, float] = {}  # Candy type -> preference (0-1)
        self.believed_values: Dict[str, float] = {}  # Candy type -> believed value
        self.inventory: Dict[str, int] = {}  # Candy type -> quantity
        self.debts: Dict[str, Dict[str, int]] = {}  # Kid ID -> {Candy type: quantity}
        
        # Social attributes
        self.social_network: List[str] = []  # List of kid IDs
        self.trust_levels: Dict[str, float] = {}  # Kid ID -> trust level (0-1)
        self.trading_bloc = None  # TradingBloc reference
        
        # Personal goal
        self.personal_goal = None  # PersonalGoal reference
        
        # Memory and learning
        self.recent_trades: List[Dict[str, Any]] = []
        self.observed_strategies: Dict[str, float] = {}  # Strategy -> success rate
        
        # Timers
        self.trade_cooldown = 0.0
        self.trick_or_treat_timer = 0.0
        self.ai_tick_timer = 0.0
        
        # Movement
        self.target_position: Optional[Vector2] = None
        self.target_house = None
        self.max_speed = 50.0  # pixels per second
        
    def update(self, dt: float):
        """Update kid state and behavior."""
        super().update(dt)
        
        if not self.active:
            return
        
        # Update timers
        self.trade_cooldown = max(0, self.trade_cooldown - dt)
        self.trick_or_treat_timer = max(0, self.trick_or_treat_timer - dt)
        self.ai_tick_timer += dt
        
        # State-based behavior
        self._update_state_behavior(dt)
    
    def _update_state_behavior(self, dt: float):
        """Update behavior based on current state."""
        if self.state == KidState.MOVING_TO_HOUSE:
            if self.target_position:
                if self.move_toward(self.target_position, self.max_speed, dt):
                    self.state = KidState.TRICK_OR_TREATING
                    self.trick_or_treat_timer = 2.0  # Spend 2 seconds trick-or-treating
        elif self.state == KidState.TRICK_OR_TREATING:
            if self.trick_or_treat_timer <= 0:
                self.state = KidState.IDLE
        elif self.state == KidState.SEEKING_TRADE:
            # Movement handled in AI tick
            pass
    
    def ai_tick(self, world):
        """
        Heavy AI logic that runs every 2-3 seconds.
        
        Args:
            world: GameWorld reference for accessing other entities
        """
        if not self.active:
            return
        
        # Check debt obligations first
        if self._has_overdue_debt():
            self._seek_debt_repayment(world)
            return
        
        # Goal-driven behavior
        if self.personal_goal and self.personal_goal.is_urgent():
            self._pursue_goal(world)
            return
        
        # Default: Trade or trick-or-treat
        import random
        if random.random() < 0.3:  # 30% chance to seek house
            self._pick_new_house(world)
        else:
            self._seek_trade_partner(world)
    
    def _has_overdue_debt(self) -> bool:
        """Check if kid has overdue debt."""
        # Placeholder implementation
        return False
    
    def _seek_debt_repayment(self, world):
        """Seek to repay overdue debt."""
        # Placeholder implementation
        pass
    
    def _pursue_goal(self, world):
        """Pursue personal goal."""
        if not self.personal_goal:
            return
        # Placeholder implementation
        pass
    
    def _pick_new_house(self, world):
        """Pick a new house to visit for trick-or-treating."""
        # Placeholder implementation
        self.state = KidState.IDLE
    
    def _seek_trade_partner(self, world):
        """Seek a trading partner."""
        # Placeholder implementation
        self.state = KidState.IDLE
    
    def evaluate_trade(self, offer: Dict[str, int], request: Dict[str, int]) -> float:
        """
        Evaluate a trade proposal.
        
        Args:
            offer: What this kid would give
            request: What this kid would receive
            
        Returns:
            Trade score (>0 = accept, <0 = reject)
        """
        # Placeholder implementation
        return 0.0
    
    def hear_rumor(self, rumor):
        """Process a rumor and update beliefs."""
        # Placeholder implementation
        pass
    
    def observe_trade(self, other_kid, trade_data):
        """Observe another kid's trade and learn from it."""
        # Placeholder implementation
        pass
    
    def add_candy(self, candy_type: str, quantity: int):
        """Add candy to inventory."""
        if candy_type not in self.inventory:
            self.inventory[candy_type] = 0
        self.inventory[candy_type] += quantity
    
    def remove_candy(self, candy_type: str, quantity: int) -> bool:
        """
        Remove candy from inventory.
        
        Returns:
            True if successful, False if not enough candy
        """
        if candy_type not in self.inventory or self.inventory[candy_type] < quantity:
            return False
        self.inventory[candy_type] -= quantity
        return True
    
    def has_candy(self, candy_type: str, quantity: int = 1) -> bool:
        """Check if kid has enough of a candy type."""
        return self.inventory.get(candy_type, 0) >= quantity
    
    def get_total_candy_value(self, real_values: Dict[str, float]) -> float:
        """Calculate total value of kid's candy inventory."""
        total = 0.0
        for candy_type, quantity in self.inventory.items():
            if candy_type in real_values:
                total += real_values[candy_type] * quantity
        return total
    
    def render(self, screen, camera=None):
        """Render the kid."""
        super().render(screen, camera)
        
        if not self.visible or not self.active:
            return
        
        # Placeholder rendering - will be implemented in later sprints
        # For now, just render a colored circle
        import pygame
        
        # Convert world position to screen position
        if camera:
            screen_pos = camera.world_to_screen(self.position)
        else:
            screen_pos = self.position
        
        # Draw kid as a colored circle
        color = self._get_mood_color()
        pygame.draw.circle(screen, color, screen_pos.to_int_tuple(), 10)
    
    def _get_mood_color(self) -> tuple:
        """Get color based on current mood."""
        mood_colors = {
            Mood.HAPPY: (100, 255, 100),
            Mood.NEUTRAL: (255, 255, 255),
            Mood.ANXIOUS: (255, 255, 100),
            Mood.GREEDY: (255, 100, 255),
            Mood.PANIC: (255, 100, 100)
        }
        return mood_colors.get(self.mood, (255, 255, 255))
