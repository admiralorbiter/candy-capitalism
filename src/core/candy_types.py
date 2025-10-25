"""
Candy type definitions and visual properties.

Defines candy types, their colors, and visual representations.
"""

from typing import Dict, Tuple
from ..core.config_manager import config_manager


class CandyTypes:
    """Manages candy type definitions and visual properties."""
    
    # Candy type colors (RGB tuples)
    CANDY_COLORS = {
        "chocolate": (139, 69, 19),    # Brown
        "fruity": (255, 192, 203),     # Pink
        "sour": (255, 255, 0),         # Yellow
        "mint": (0, 255, 127),         # Green
        "caramel": (255, 165, 0),      # Orange
        "licorice": (75, 0, 130),      # Purple
        "trash": (128, 128, 128),      # Gray
        "health": (0, 255, 0),         # Bright Green
        "novelty": (255, 20, 147)      # Hot Pink
    }
    
    # Candy type icons (single characters for now)
    CANDY_ICONS = {
        "chocolate": "C",
        "fruity": "F",
        "sour": "S",
        "mint": "M",
        "caramel": "A",
        "licorice": "L",
        "trash": "T",
        "health": "H",
        "novelty": "N"
    }
    
    # Fallback for unknown candy types
    DEFAULT_COLOR = (255, 255, 255)  # White
    DEFAULT_ICON = "?"  # Generic candy
    
    @classmethod
    def get_color(cls, candy_type: str) -> Tuple[int, int, int]:
        """Get color for a candy type."""
        return cls.CANDY_COLORS.get(candy_type, cls.DEFAULT_COLOR)
    
    @classmethod
    def get_icon(cls, candy_type: str) -> str:
        """Get icon for a candy type."""
        return cls.CANDY_ICONS.get(candy_type, cls.DEFAULT_ICON)
    
    @classmethod
    def get_all_types(cls) -> list:
        """Get list of all candy types."""
        return list(cls.CANDY_COLORS.keys())
    
    @classmethod
    def get_visual_properties(cls, candy_type: str) -> Dict[str, any]:
        """Get all visual properties for a candy type."""
        return {
            "color": cls.get_color(candy_type),
            "icon": cls.get_icon(candy_type),
            "name": candy_type.title()
        }
    
    @classmethod
    def load_from_config(cls):
        """Load candy types from configuration file."""
        try:
            candy_config = config_manager.get('candy_types')
            if candy_config:
                # Update colors from config if available
                for candy_type, properties in candy_config.items():
                    if 'color' in properties:
                        cls.CANDY_COLORS[candy_type] = tuple(properties['color'])
                    if 'icon' in properties:
                        cls.CANDY_ICONS[candy_type] = properties['icon']
        except Exception as e:
            print(f"Warning: Could not load candy types from config: {e}")


# Initialize candy types from config
CandyTypes.load_from_config()
