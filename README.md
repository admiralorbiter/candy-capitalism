# Candy Capitalism - Documentation Summary

## Overview

Welcome to **Candy Capitalism**! This package contains complete design documentation for a Halloween-themed economic manipulation game. You play as a market demon (the "invisible hand") manipulating trick-or-treating children and their candy economy.

---

## Document Guide

### 1. **Game Design Document** (`candy_economy_gdd.md`)
**What it is**: Complete game design covering all systems, mechanics, and features.

**Key Sections**:
- Core gameplay loops (minute-to-minute, hour-to-hour, session-to-session)
- 13 interconnected systems (trading, possession, rumors, supply, cartels, etc.)
- Scenarios and game modes
- UI design (minimal, backend-focused)
- Technical architecture overview
- Art and sound requirements

**Read this if**: You want to understand what the game is and how it plays.

---

### 2. **Sprint Breakdown** (`candy_economy_sprints.md`)
**What it is**: 18-week development plan broken into 9 two-week sprints.

**Key Sections**:
- Sprint 0: Setup (3-5 days)
- Sprints 1-2: Core movement and trading (4 weeks)
- Sprint 3: Possession and supply manipulation (2 weeks)
- Sprint 4: Rumors and combo system (2 weeks)
- Sprint 5: Debt, mood, and personal goals (2 weeks)
- Sprint 6: Cartels and behavior contagion (2 weeks)
- Sprint 7: Scenarios, events, and progression (2 weeks)
- Sprint 8: Polish and launch prep (2 weeks)
- Sprint 9: Sandbox mode and advanced features (2 weeks)

**Read this if**: You're ready to start development and need a structured plan.

---

### 3. **Systems & Engine Design** (`candy_capitalism_systems_engine.md`)
**What it is**: Deep technical dive into implementation details for Pygame.

**Key Sections**:
- Engine architecture and game loop
- AI architecture (FSM, behavior trees)
- Economy and trading algorithms
- Data structures (spatial partitioning, pathfinding, rumor propagation)
- Performance optimization strategies
- Event system architecture
- UI implementation patterns
- Save/load system
- Debugging tools
- Testing strategies

**Read this if**: You're implementing the game and need technical guidance.

---

## Key Improvements Made

### New Systems Added (Beyond Original Scope)

1. **Supply Manipulation** ⭐⭐⭐
   - Curse/Bless houses to control supply
   - Creates artificial scarcity you can exploit
   - Adds proactive market control alongside demand manipulation

2. **Price Discovery Phase** ⭐⭐⭐
   - Kids start with no knowledge of candy values
   - Wild West early game with terrible trades
   - Market gradually discovers true values (or you prevent it)
   - Creates distinct early/mid/late game phases

3. **Cartel/Alliance Formation** ⭐⭐⭐
   - Kids form trading blocs based on social networks
   - Inside traders get information advantage
   - Natural faction warfare emerges
   - "Destroy the Chocolate Cartel" scenarios

4. **Personal Goals System** ⭐⭐
   - Each kid has a goal (collect all types, get 10 romantic candies, etc.)
   - Goals override rational behavior (exploitable)
   - Adds personality without complex AI
   - Makes manipulation feel more meaningful

5. **Behavior Contagion** ⭐⭐
   - Kids copy successful strategies they observe
   - Creates fads and behavioral waves
   - "Monkey see, monkey do" dynamics
   - Your actions can start epidemics

6. **Combo Recognition System** ⭐⭐⭐
   - Pattern matching rewards clever strategies
   - "Short Squeeze", "Pump and Dump", "Debt Bomb" etc.
   - Teaches depth through positive reinforcement
   - Satisfying feedback for mastery

7. **Random Events** ⭐⭐
   - Parent Patrol, Rain, Bullies, Mystery Houses, Recalls
   - Forces adaptation and creates opportunities
   - Adds replayability and chaos
   - Can't be controlled (pure external pressure)

### UI Improvements

8. **Quick Stats Overlay** (Hold TAB)
   - Richest kid, biggest hoarder, most debt
   - Market momentum, active cartels
   - Next event countdown
   - Helps track macro trends at a glance

9. **Chaos Score Breakdown**
   - Shows point values before actions
   - Makes scoring transparent
   - Encourages strategic point optimization

---

## Development Timeline

### Minimum Viable Product (14 weeks)
- End of Sprint 7
- Core systems + scenarios
- No sandbox or advanced features

### Full v1.0 (16 weeks)
- End of Sprint 8
- Polished and launch-ready
- All core features complete

### Deluxe Edition (18 weeks)
- End of Sprint 9
- Sandbox mode with parameter sliders
- Advanced features and replayability

---

## Quick Start Checklist

### Before You Begin
- [ ] Read the Game Design Document (skim at minimum)
- [ ] Review Sprint 0 for setup requirements
- [ ] Read "Engine Architecture" section in Systems doc
- [ ] Set up development environment (Pygame, Python 3.10+)

### Sprint 1 Focus
- [ ] Basic pygame window and game loop
- [ ] Kid and House entities
- [ ] Autonomous movement with simple pathfinding
- [ ] Top-down rendering

**Goal**: 10 kids walking around a neighborhood automatically.

### Success Markers
- **Week 4**: Kids trading autonomously based on preferences
- **Week 6**: Can possess kids and force bad trades
- **Week 8**: Rumors spread and affect market
- **Week 10**: Debt cascades and moods working
- **Week 12**: Cartels form naturally, behavior spreads
- **Week 14**: Tutorial + 3 scenarios playable
- **Week 16**: Polished and ready for feedback

---

## Core Philosophy

### Systems Over Graphics
- Invest in robust AI and economy simulation
- UI can be simple, emergence must be spectacular
- Backend-heavy is your strength - leverage it

### Emergence Over Scripting
- Simple rules create complex behavior
- No scripted events, just systems interacting
- Players discover strategies you didn't plan

### Incremental Complexity
- Start simple (movement + trading)
- Add one system at a time
- Playtest for emergence at each stage
- Each sprint builds on previous work

### Flexible Scope
- Can ship after Sprint 7 if needed
- Modular design allows feature cuts
- Post-launch updates are viable

---

## Key Differentiators

What makes Candy Capitalism special:

1. **Economic Warfare as Core Mechanic** - Not just a side system
2. **Villain Protagonist** - Playing as a market demon is fun
3. **Indirect Control** - Puzzle-like optimization rather than direct RTS
4. **Combo System** - Teaches depth through positive rewards
5. **Price Discovery** - Creates distinct game phases naturally
6. **Emergent Cartels** - Faction warfare without scripting
7. **Halloween Theme** - Unique aesthetic rarely seen in economy sims
8. **Information Warfare** - Rumors and beliefs separate from reality

---

## Technical Highlights

### Performance Targets
- 60 FPS with 30+ kids
- AI updates at 0.5 Hz (every 2 seconds)
- Spatial partitioning for O(1) neighbor queries
- Object pooling for frequently allocated objects

### Architecture Patterns
- Event-driven for system decoupling
- State machine for game flow
- Entity-Component-System inspired
- JSON configs for easy tuning

### Optimization Strategy
- Tiered update frequencies (per frame vs per AI tick vs slow updates)
- Pathfinding caching
- Text rendering caching
- Profiling hooks for debugging

---

## Risk Mitigation

### High Risk Items
1. **AI Balance** - Making kids smart but exploitable
   - Mitigation: Extensive testing, tunable parameters in JSON
   
2. **Performance** - 30 AI agents running simultaneously
   - Mitigation: Spatial grid, tiered updates, profiling

### Medium Risk Items
1. **Player Confusion** - Indirect control might feel powerless
   - Mitigation: Clear feedback, tutorial, combo system rewards
   
2. **Runaway Economies** - Too stable or too chaotic
   - Mitigation: Tunable params, decay system, playtesting

---

## Post-Launch Roadmap

### Update 1.1: Community
- Online leaderboards
- Share sandbox configs
- Replay system

### Update 1.2: More Content
- New scenarios
- New random events
- Holiday themes

### Update 1.3: Advanced Economics
- Stock market mechanics
- Insurance systems
- Futures trading (if not in v1.0)

### Update 1.4: Meta Progression
- Permanent unlocks
- Prestige system
- Daily challenges

---

## Development Best Practices

### Weekly Routine
- **Monday**: Plan week's tasks, review last week
- **Wednesday**: Mid-sprint check, adjust if needed
- **Friday**: Commit working build, playtest, retrospective

### Playtesting Cadence
- End of every sprint (even incomplete)
- Mid-project external playtest (after Sprint 4)
- Extensive testing in Sprint 8

### When to Ask for Help
- If sprint runs 50%+ over time
- If core loop isn't fun by Sprint 4
- If performance is below target by Sprint 6

---

## Success Metrics

### Must Hit
- [ ] Tutorial completion rate > 80%
- [ ] Average session length > 20 minutes
- [ ] Runs at 60 FPS with 30 kids
- [ ] Zero critical bugs

### Nice to Have
- [ ] Players discover unintended combos
- [ ] Memorable "war stories" from chaotic runs
- [ ] Each scenario requires different strategy
- [ ] Sandbox mode is endlessly replayable

---

## Final Words

**Candy Capitalism** is scoped for solo development over 16-18 weeks. The focus on emergent behavior from simple rules means your backend strengths are perfectly suited to this project.

The modular sprint structure allows flexibility - you can ship early, cut features, or expand post-launch. The most important thing is getting the core trading AI and price discovery working well. Everything else enhances that core loop.

The combo system and cartel formation are your "secret sauce" - they make the systems feel cohesive and reward mastery. Don't skimp on these even if you need to cut other features.

Start with Sprint 1, validate the fun early, and iterate. The game rewards mastery of interconnected systems - beginners cause chaos, experts orchestrate economic warfare.

**Good luck, and may your candy markets crash spectacularly!**

---

## Quick Reference

### File Sizes
- Game Design Document: ~30KB (comprehensive overview)
- Sprint Breakdown: ~34KB (18-week development plan)
- Systems & Engine Design: ~40KB (technical deep dive)

### Contact Points for Questions
When implementing, refer to:
- **"How does X system work?"** → Game Design Document
- **"When should I build X?"** → Sprint Breakdown
- **"How do I implement X?"** → Systems & Engine Design

### Version
- Documentation Version: 1.0
- Target Game Version: 1.0
- Last Updated: October 2025
