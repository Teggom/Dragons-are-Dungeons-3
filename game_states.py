from enum import Enum

class GameStates(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    GRAPHICAL = 3
    MAIN_MENU = 4
    CHARACTER_SELECT = 5
    