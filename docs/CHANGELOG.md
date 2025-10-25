# Candy Capitalism - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Sprint 1: Core World & Movement
- Sprint 2: Core Trading System
- Sprint 3: Possession System & Basic UI
- Sprint 4: Rumor System
- Sprint 5: Debt & Mood Systems
- Sprint 6: Cartels, Behavior Contagion & Personality Polish
- Sprint 7: Scenarios, Random Events & Progression
- Sprint 8: Polish, Juice & Launch Prep
- Sprint 9: Sandbox Mode & Advanced Features

## [0.1.0] - 2025-10-25

### Added
- **Sprint 0: Project Setup** - Complete foundation for Candy Capitalism development

#### Core Architecture
- Game loop with 60 FPS target
- State machine for game states (MAIN_MENU, PLAYING, PAUSED, etc.)
- Configuration management system with JSON configs
- Event-driven communication system
- Spatial partitioning for performance optimization

#### Entity System
- Base entity class with position, velocity, and update/render hooks
- Kid entity with AI states, personality types, and trading capabilities
- House entity with candy dispensing and power effects (curse/bless)
- Rumor entity for information warfare
- Trading bloc entity for cartel formation

#### Game Systems
- Economy system with price discovery and market dynamics
- Possession system for player control of kids
- Rumor system for spreading misinformation
- Event system for decoupled communication
- Game world coordinator managing all entities and systems

#### Utilities
- Vector2 class for 2D math operations
- Spatial grid for efficient neighbor queries
- Helper functions for common operations
- Coordinate conversion utilities

#### Rendering Foundation
- Renderer class for world rendering
- Camera system for world-to-screen conversion
- UI manager with layered rendering
- Base UI element classes

#### Configuration
- Candy types configuration (6 types with values and properties)
- Game settings (screen size, FPS, AI rates, etc.)
- Personality types configuration
- Extensible JSON-based config system

#### Testing
- Pytest configuration and fixtures
- Unit tests for economy system
- Integration tests for trading system
- Test structure for future development

#### Documentation
- Development philosophy document
- Technical architecture overview
- Sprint progress tracking
- Comprehensive code documentation

#### Project Structure
```
/src
  /core          - Game loop, managers, constants
  /entities      - Kid, House, Rumor, TradingBloc
  /systems       - Economy, Possession, Rumor, Event
  /ai            - AI behaviors and decision making
  /ui            - User interface elements
  /rendering     - Renderer, camera, sprite manager
  /utils         - Vector2, spatial grid, helpers
/config          - JSON configuration files
/assets          - Art and audio assets
/tests           - Unit and integration tests
/docs            - Development documentation
```

### Technical Details
- **Python Version**: 3.12.0
- **Engine**: Pygame >= 2.5.0
- **Testing**: Pytest >= 7.4.0
- **Architecture**: Event-driven, modular design
- **Performance**: 60 FPS target with 30+ AI agents
- **Update Frequencies**: 60 FPS rendering, 0.5 Hz AI, 0.1 Hz slow updates

### Success Criteria Met
- [x] Game window opens and runs at 60 FPS with empty scene
- [x] Project structure supports modular development
- [x] All skeleton files have docstrings and basic structure
- [x] Config loading works
- [x] Documentation clearly explains development approach
- [x] Test structure in place with example tests
- [x] Foundation ready for Sprint 1 development

### Known Issues
- Rendering system is placeholder (will be implemented in Sprint 1)
- AI behavior is placeholder (will be implemented in Sprint 2)
- Trading system is placeholder (will be implemented in Sprint 2)
- No actual gameplay yet (foundation only)

### Next Release
- **v0.2.0** - Sprint 1: Core World & Movement
  - Neighborhood map generation
  - Kid autonomous movement
  - Basic pathfinding
  - House candy dispensing
  - 10+ kids moving around neighborhood

---

## Development Notes

### Sprint 0 Completion
This release represents the complete foundation for Candy Capitalism. All core architecture is in place, including:

1. **Modular Design**: Clean separation of concerns with short, focused files
2. **Event-Driven**: Loose coupling between systems via event bus
3. **Performance-First**: Spatial partitioning and tiered update frequencies
4. **Configuration-Driven**: All tunable values in JSON configs
5. **Test-Ready**: Comprehensive test structure with examples
6. **Documentation**: Clear philosophy and architecture guides

The project is now ready for Sprint 1 development, which will focus on implementing the core world and movement systems to create the first playable version.

### Key Architectural Decisions
- **Pygame**: Chosen for simplicity and 2D performance
- **Python**: Rapid prototyping and AI/data processing
- **Event Bus**: Enables loose coupling and easy feature addition
- **Spatial Grid**: Essential for 30+ entity performance
- **JSON Configs**: Easy tuning without code changes
- **Modular Files**: Each file has single responsibility

### Performance Targets
- **Rendering**: 60 FPS with simple 2D graphics
- **AI Updates**: 0.5 Hz (every 2 seconds) for 30+ kids
- **Spatial Queries**: O(1) neighbor finding via grid
- **Memory**: Object pooling for frequent allocations
- **Scalability**: Support for 30+ kids, 25+ houses

This foundation provides a solid base for building the complex economic simulation that will make Candy Capitalism unique and engaging.
