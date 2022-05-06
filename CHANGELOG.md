# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.0.17] - 2022-05-04

### Added 
- New Skills and Stats...
  - Added to Equipment menu windows
  - Have leveling set up
  - Have proper references set up
- "What you know" Menu
  - Shows things that your perception stat is high enough to see

### Changed
- Re-enabled message feed

## [0.0.17] - 2022-05-06

### Added
- Message feed is back along the bottom of the main map
- Map Info Panel on the right side of the screen
  - Top part displays player meta information
    - Name/Race/Class/Weapons/Gear Score/"Score"/HP/MP
  - Middle part displays item meta information
    - Shows item/entity sprites that are in the FOV
    - , or . to cycle pages 
    - Sorted by Rarity
      - / to toggle sort mode (A-Z, Distance)
  - Bottom part displays character meta information
    - Shows enemies/NPC/affiliation and such
    - < or > to cycle pages
    - Sorted by Est. Difficulty
      - ? to toggle sort mode (A-Z, Distance)
- Items have value now
  - Value is dynamic, just judges how much that item is worth.


## [0.0.16] - 2022-05-02

### Added
- Noise stat (Below is stuff it will be used for)
  - Will be used for enemy states
  - Items carry noise
  - Traits and Conditions can lower noise
  - Noise can alert enemies
    - Enemies will enter a searching state rather than an idle state and will perform perception checks each turn as they move towards the source
  - Some spells or use items can create noise
  - No formula for noise yet
- Weapon types
  - Weapon types that can level are as follows
    - sword, dagger, greatsword, axe, hammer, whip, flail, spear, halberd, scythe, fist, bow, crossbow, staff, wand
  - Weapon types that cannot level are as follows
    - shield, greatshield, non-weapon
      - non-weapon fills category such as charm/torch/bell
      - shields provide no damage (usually?)
- Four new skills in the works
  - Mining, Harvesting, Enchanting, Summoning

### Changed
- Weapon type is now displayed on the item card menu

### Fixed
- Removed already-moved files from git

## [0.0.15] - 2022-05-01

### Changed
- Upgraded Traits and Items
  - Removed old traits and items
  - Traits are now well defined structures
    - Items properly reference all new elements of traits
- Items
  - Items can have 1 trait max
    - Changes the item's name
  - Items can have multiple conditions
  - Items now have PERTURN, PERUSE, ONHIT functions
    - Per Turn will activate every turn the item is equipped
    - Per Use will activate for items when they are used
    - On hit will activate for items when they hit another entity
- Traits
  - Traits behave differently depending on where they are
    - Traits contain categories for "on_char" and "on_item", both contain skills/stats/resistances
    - "on_char"
      - perturn functions
        - Activate when the trait's attached item is equipped each turn
      - perturn damage
        - Activate when the trait's attached item is equipped and deals damage to equipper
    - "on_item"
      - perturn functions
        - Activates when the traits attached item is equipped each turn
      - onhit damage
        - Extra damage given to the item if it is on a weapon.
          - Sword -> Sword of Fire. Sword of Fire shows extra fire damage stat
      - onhit enemy func
        - Activates when the equipped item attacks an enemy successfully
          - Sword of flaming has a chance to light enemies on fire. 

## [0.0.14] - 2022-04-28

### Changed
- sdl_rendering is now used for everything. Changes from this are as follows
  - This allows multiple tilesets to be rendered in the same frame
  - Multiple tilesets added. Huge credit to Dwarf Fortress wiki for supplying them
    - Map tileset is now 32x32 (for now)
    - Text tileset is now 16x10
    - Title tileset is now 48x48 (for now)
  - Title is now much larger and RED
  - Map is now a huge grid of 32x32 tiles
    - Menus render on top of the map as before, and are of the text tileset

### Fixed
- Updated cursor UI so selected elements are black on yellow


## [0.0.13] - 2022-04-21

### Added
- Visible Health and Mana Bar
- Message Log

### Changed
- Ascii pack is different now
  - Items have a few custom Ascii(s)
- Items now take a dict for char and color
  - Eventual goal will be: 
    - Create Sword X. 
    - Sword x gets Char '/' and color silver
    - Can sword X have any applied things? Like of fire? 
      - If so, apply one randomly
      - If "of fire" is on a weapon, add a damage type and change color to red. 
    - Place sword
- Menu bar is now different
  - u opens equipment
  - keys are highlighted in yellow
    - Looks nice in Qud
  - new menu options (not implmented)
- Movement keys have changed
  - Arrow keys work. However
    - wdxa are now valid substitutes
    - qezc allow diagonal movement
    - s will be a stand in for wait/search
      - Might swap s and x if it isn't comfortable

### Fixed
- Removed unused folder unit_stats/ from repo


## [0.0.12] - 2022-04-20

### Added
- Resistances window in equipment menu
- Two new slots for Rings
  - Left Ring
  - Right Ring

### Changed
- Tab now cycles through equipment menu windows
  - Stats, Skills, Resistances
- Item window shows Item's stats and information dynamically
  - No longer a fixed size, shows no irrelevant stats
- Item window now displays damage values and averages

### Fixed
- Duel-handing weapons with equipment now display correct stats
  - Having a "two handed" axe in your right hand
    - Equiping a 'two handed' axe in your left hand shows correct difference
    - Equiping a 'one handed' weapon in either hand shows correct difference
  - When trying to equip a two handed weapon
    - Correct stats show for any permutation of equipment

## [0.0.11] - 2022-04-19

### Added
- Resistances
  - Magic-Oriented
    - Fire, Frost, Shock, Arcana, Poison, Holy, Unholy
  - Physical-Oriented
    - Blunt, Slash, Pierce
  - Catchall
    - Pure
  - Equipment, Traits, Conditions can all apply resistances
  - Formula for applying damage is ceiling(damage*(1-x/(x+20)))
    - where x is your resistance
    - negative resistance causes you to take extra damage
- Page_up / Page_down
  - Equipment menu bag
  - Ground menu
- Equipment menu now has item details screen
  - Shows resistances, other stats, and placeholders for goodies
  
### Changed
- HP and MP can now level
  - MP exp is gained when spending mp
  - HP exp is gained when taking damage before modifiers


## [0.0.10] - 2022-04-16

### Added
- 11 Skills
  - Scaling in Stat and Skill Overview
  - Athletics: Checks on physically doing something
  - Acrobatics: Checks on body reactions
  - Slight of Hand: From Stealing to grabbing items. Checks involving precision
  - Stealth: Higher stealth -> Harder to be seen
    - Counters Perception
  - Arcana: Spellcasting checks for branch magic (not Cantrips)
  - Alchemy: Liquid identification and creation checks
  - Crafting: general crafting + workshop skill
  - Bartering: Lowers prices at shops + more likeable
  - Persuasion: Skill of convincing with Wisdom scaling
  - Intimidation: Skill of convincing with Strength scaling
  - Deception: Skill of convincing with Int scaling
- Leveling
  - All primary stats and skills can now level
- Equipment menu now has screen with stats


### Fixed
- Dropping items from equipment menu behaves as expected
  - And they end up below you on the map!
- Unequiping items behaves as expected
- Squashed annoying print message

## [0.0.9] - 2022-04-14

### Added
- Top Banner
  - Shows you some menus you can bring up, as well as the button for those menus
- Ground Menu [g]
  - Displays things at your feet
  - Will eventually perform a search check as well
  - Buttons
    - Arrow keys to move
    - enter to pick up item
    - esc/g to back out to the game
- Equipment Menu [e]
  - Two screens, shows your currently worn items
    - Needs to show stat changes as well (TODO)
  - Buttons
    - Arrow Keys to move
    - Right arrow key or Enter will access bag for highlighted gear slot
      - Arrow keys to move
      - Enter to equip
    - d will drop or unequip an item depending on what screen you're on
      - BUGGED
    - Equipment will be displayed as stacked if multiple exist
    - Currently no way to sort
    - Windows scale with number of items in bag
      - Will be rolled out and page up/down will be used to scroll through bags
- Inventory (No menus or handling set up)
- Map (No menus or handling set up)
- Need to add "Character [c]" Screen






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
