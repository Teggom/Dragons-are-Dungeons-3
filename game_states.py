from enum import Enum

from unit_components.inventory import Inventory

class GameStates(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    GRAPHICAL = 3
    MAIN_MENU = 4
    CHARACTER_SELECT = 5
    GROUND_MENU = 6 # Looks at the ground
    EQUIPMENT_MENU = 7
    INVENTORY_MENU = 8