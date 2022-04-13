# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).



## [0.0.8] - 2022-04-13

### Added
- Larger, scrolling maps
  - Game is now rendered from the camera view

### Changed
- Removed monsters for the time being
  - Until they can be killed, they block paths

## [0.0.7] - 2022-04-11

### Added
- Main Menu
- Character Select
  - Lets you start as different races!
    - Classes not implemented

### Changed
- Esc key doesn't exit game unless you're at the main menu



## [0.0.6] - 2022-04-09

### Added
- Inventory and Items! (Bug Free!)
  - Functionallity
    - Equiping
    - Unequiping
    - Stacking
    - Twohanding
    - Gold!
  - Items can have conditions (poison/chill/burn arrows or weapons)
  - Items can have traits (perm things affecting skills or stats)
  - Wearing Slots:
    - Head, Neck, Chest, Back, L. Arm, R. Arm, L. Hand, R. Hand, Belt, Legs, L.Foot, R. Foot
  - Bag Slots:
    - Head, Neck, Chest, Back, Arm, Weapon, Belt, Legs, Feet, Item
- Damage Objects
  - parses damage strings
    - "3d5+10"
  - For weapons
- Extra text file in <code>/General_Readmes/Stats/Stat and Skill Overview.txt</code>
  - Moved prior text file there
  
### Changed
- Elves now start with debt





## [0.0.5] - 2022-04-08

### Added
- Nice explanation at /unit_stats/Stat Breakdown.txt
- Additional Skills (I keep calling them stats)
  - Skills are based on core stats, and scale up off them
- Skill rollup functions
- Skill Bonus Level Calculation functions are now defined
  - See Stat Breakdown

### Changed
- Stat rollup functions
- Window title



## [0.0.4] - 2022-04-07
 
### Added
- Death system
- Perception Stat
  - Will be used for look-around and identify
  - Certain things will be unseen with low enough perception
    - Given Door
      - Perception of 10 reveals it is made of stone and locked
      - Perception of 5 reveals it is made of stone
      - Perception of 1 might miss that there is a door
        - ? identifier on map maybe?
    - Applies to things like Disguises
- Traits
  - Traits are currently perm modifiers on your character
  - You can have any number of traits
  - Traits add or remove from other stats
  - Current traits
    - Blindness, Supervision (Affect FOV)
    - Dory, Photomem (Affect memory)
- Conditions
  - Derived from traits
  - Expire after a certain amount of time
  - Player currently receives a temp blindness debuff after 10 steps
    - Only lasts 10 steps

### Changed
- Made Elves Blind
- Made Elves have the memory of a certain blue fish

### Fixed
- Elves now have a small chance to outright die every turn
  - about 1 in 4



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
