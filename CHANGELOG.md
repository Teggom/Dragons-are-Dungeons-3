# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [0.0.3] - 2022-04-05
General Advancement

### Added
- Some functions for testing out animations
- Simple Enemies
  - Goblin, Orc, Troll
- AI for NPCs
  - Wander
  - Basic Merchant
  - basic Monster
    - With A*
- Elves now scream and run into walls

### Changed
- Player is now a Goblin by Default
- FOV and Memory are now their own stats
  - FOV is euclidean distance
  - Memory maintains the same modifier for now. 
    - <code>player.stats.memory**4</code> 
  - Both of these stats are now defined by race




## [0.0.2] - 2022-04-04
Some early graphical changes, stats, and early races

### Added
- Color Gradients to tiles
  - Gradiants are harsher for non-wall tiles.
- Added class component for entities, giving units useless stats (for now!)
  - Added getter methods for stats
    - Will help when 5 spells, 3 traits, 5 pieces of gear and 2 debuffs affect strength
  - Added Race Dependant Stats
- Map Forgetting is currently dependant on <code>4^player.intelligence</code>. 
  - Might be worthwhile to add a specific stat for map rememberence, and checking if there are any items or other things that influence it.
    - Feels messed up that a dwarf wouldn't be able to remember the way



## [0.0.1] - 2022-04-02
 
The initial push towards a git repo, private for now. Future code will be modified from this to shape the game into my vision. 
 
### Added
- Codebase from old [Roguebasin](http://www.roguebasin.com/) tutorial, but on a [new website](http://rogueliketutorials.com/tutorials/tcod/v2/)
  - Branched from part 3
- CHANGELOG.md
- README.md
- Depending on Character Stats, things will be forgotten over time. 
