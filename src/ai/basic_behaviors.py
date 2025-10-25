"""
Basic AI behaviors for kids.

Implements simple decision-making logic for house selection,
trick-or-treating, and basic movement patterns.
"""

import random
from typing import List, Optional
from ..entities.kid import Kid, KidState
from ..entities.house import House
from ..utils.vector2 import Vector2


class BasicBehaviors:
    """
    Basic AI behaviors for kids.
    
    Implements simple decision-making without complex pathfinding.
    """
    
    @staticmethod
    def select_house(kid: Kid, world) -> Optional[House]:
        """
        Select a house for trick-or-treating.
        
        Args:
            kid: Kid entity making the decision
            world: GameWorld instance
            
        Returns:
            Selected house or None if no valid houses
        """
        if not world.houses:
            return None
        
        # Filter out houses on cooldown
        available_houses = [house for house in world.houses if house.is_available()]
        
        if not available_houses:
            return None
        
        # Simple selection: pick random available house
        # Later this could be based on house quality, distance, etc.
        return random.choice(available_houses)
    
    @staticmethod
    def should_visit_house(kid: Kid, house: House) -> bool:
        """
        Determine if kid should visit a specific house.
        
        Args:
            kid: Kid entity
            house: House to consider
            
        Returns:
            True if kid should visit this house
        """
        # For now, always visit houses
        # Later this could consider:
        # - Distance to house
        # - House quality
        # - Kid's mood and preferences
        # - Whether house is cursed/blessed
        return True
    
    @staticmethod
    def calculate_house_attraction(kid: Kid, house: House) -> float:
        """
        Calculate how attractive a house is to a kid.
        
        Args:
            kid: Kid entity
            house: House to evaluate
            
        Returns:
            Attraction score (0.0 to 1.0)
        """
        # Base attraction from house
        base_attraction = house.get_attraction_strength(kid.position)
        
        # Modify based on kid's personality
        personality_modifier = BasicBehaviors._get_personality_house_preference(kid, house)
        
        # Modify based on distance (closer is better)
        distance = kid.position.distance_to(house.position)
        max_distance = 500.0  # Maximum distance to consider
        distance_factor = max(0.0, 1.0 - (distance / max_distance))
        
        # Combine factors
        final_attraction = base_attraction * personality_modifier * distance_factor
        
        return min(1.0, final_attraction)
    
    @staticmethod
    def _get_personality_house_preference(kid: Kid, house: House) -> float:
        """Get house preference modifier based on kid's personality."""
        # High-quality houses are more attractive to certain personalities
        if kid.personality.name == "VALUE_INVESTOR":
            # Value investors prefer high-quality houses
            return 0.5 + (house.quality * 0.2)
        elif kid.personality.name == "HOARDER":
            # Hoarders prefer any house that gives candy
            return 1.0
        elif kid.personality.name == "SOCIAL_TRADER":
            # Social traders prefer houses where other kids are
            # (simplified: prefer mid-quality houses)
            return 0.8 if house.quality == 2 else 1.0
        else:
            # Default: slight preference for higher quality
            return 0.7 + (house.quality * 0.1)
    
    @staticmethod
    def execute_trick_or_treat(kid: Kid, house: House, renderer=None) -> bool:
        """
        Execute trick-or-treating at a house.
        
        Args:
            kid: Kid entity
            house: House being visited
            renderer: Optional renderer for particle effects
            
        Returns:
            True if successful, False otherwise
        """
        if not house.can_dispense_candy():
            return False
        
        # Get candy from house
        candy_given = house.dispense_candy()
        
        if not candy_given:
            return False
        
        # Add candy to kid's inventory
        for candy_type, quantity in candy_given.items():
            kid.add_candy(candy_type, quantity)
        
        # Emit particles for visual feedback
        if renderer:
            # Use the first candy type for particle color
            first_candy_type = list(candy_given.keys())[0] if candy_given else "chocolate"
            renderer.emit_candy_particles(house.position, first_candy_type)
        
        # Update kid's mood based on candy received
        BasicBehaviors._update_mood_from_candy(kid, candy_given)
        
        return True
    
    @staticmethod
    def _update_mood_from_candy(kid: Kid, candy_received: dict):
        """Update kid's mood based on candy received."""
        if not candy_received:
            return
        
        # Count total candy pieces
        total_candy = sum(candy_received.values())
        
        # Update mood based on amount and quality
        if total_candy >= 3:
            # Lots of candy - make kid happy
            if kid.mood.name != "HAPPY":
                kid.mood = kid.mood.__class__.HAPPY
        elif total_candy == 1:
            # Little candy - might make kid anxious
            if kid.mood.name == "NEUTRAL":
                kid.mood = kid.mood.__class__.ANXIOUS
        # Otherwise, keep current mood
    
    @staticmethod
    def should_seek_new_house(kid: Kid) -> bool:
        """
        Determine if kid should seek a new house.
        
        Args:
            kid: Kid entity
            
        Returns:
            True if kid should seek a new house
        """
        # Simple logic: if idle for a while, seek a house
        if kid.state == KidState.IDLE:
            # 70% chance to seek house when idle
            return random.random() < 0.7
        
        # If trick-or-treating is done, seek new house
        if kid.state == KidState.TRICK_OR_TREATING and kid.trick_or_treat_timer <= 0:
            return True
        
        return False
    
    @staticmethod
    def get_movement_target(kid: Kid, world) -> Optional[Vector2]:
        """
        Get the target position for kid movement.
        
        Args:
            kid: Kid entity
            world: GameWorld instance
            
        Returns:
            Target position or None
        """
        if kid.state == KidState.MOVING_TO_HOUSE and kid.target_position:
            return kid.target_position
        
        if kid.state == KidState.SEEKING_TRADE:
            # For now, just pick a random position
            # Later this could be toward other kids
            world_width = 2000  # Get from config
            world_height = 2000
            x = random.uniform(100, world_width - 100)
            y = random.uniform(100, world_height - 100)
            return Vector2(x, y)
        
        return None
    
    @staticmethod
    def update_kid_behavior(kid: Kid, world, dt: float):
        """
        Update a kid's behavior based on current state.
        
        Args:
            kid: Kid entity to update
            world: GameWorld instance
            dt: Delta time
        """
        if kid.state == KidState.IDLE:
            if BasicBehaviors.should_seek_new_house(kid):
                house = BasicBehaviors.select_house(kid, world)
                if house and BasicBehaviors.should_visit_house(kid, house):
                    kid.target_house = house
                    kid.target_position = house.position
                    kid.state = KidState.MOVING_TO_HOUSE
                    
                    # Try to find a path using pathfinding
                    if world.pathfinding_manager and kid.use_pathfinding:
                        path = world.pathfinding_manager.find_path(kid.position, house.position)
                        if path:
                            kid.set_path(path)
                        else:
                            # No path found, clear path to use direct movement
                            kid.clear_path()
        
        elif kid.state == KidState.MOVING_TO_HOUSE:
            if kid.reached_target() and kid.target_house:
                # Arrived at house, start trick-or-treating
                kid.state = KidState.TRICK_OR_TREATING
                kid.trick_or_treat_timer = 2.0  # Spend 2 seconds at house
                kid.clear_path()  # Clear path when arriving
        
        elif kid.state == KidState.TRICK_OR_TREATING:
            if kid.trick_or_treat_timer <= 0:
                # Done trick-or-treating, go back to idle
                kid.state = KidState.IDLE
                kid.target_house = None
                kid.target_position = None
                kid.clear_path()
        
        elif kid.state == KidState.SEEKING_TRADE:
            # For now, just go to idle after a while
            # Later this will involve finding trading partners
            kid.state = KidState.IDLE
