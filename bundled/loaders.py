
from random import sample
from bundled.item_loader import make_item, place_item
from entity import Entity
from fov_functions import initialize_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from unit_components.ai import BasicMerchant, Wander
from unit_components.inventory import Inventory
import tcod as libtcod

def load_preamble(game, VERSION):
    # Size of window
    game['screen_width'] = 130
    game['screen_height'] = 60

    # Map size( Can change )
    game['map_width'] = 150#80
    game['map_height'] = 90#44

    # Camera Size 
    game['camera_width'] = game['screen_width']
    game['camera_height'] = game['screen_height']
    
    game['fov_algorithm'] = 4
    game['fov_light_walls'] = True
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(game['screen_width'], game['screen_height'], 'Dragons are Dungeons 3: {}'.format(VERSION), False)
    game['con'] = libtcod.console_new(game['screen_width'], game['screen_height'])
    game['key'] = libtcod.Key()
    game['mouse'] = libtcod.Mouse()



def load_mainmenu(game):
    game['game_state'] = GameStates.MAIN_MENU
    game['options'] = ['New Game', 'Options', 'Credits', 'Exit']
    game['cursor'] = 0

def load_charselect(game):
    game['game_state'] = GameStates.CHARACTER_SELECT
    game['cursor_0'] = 0
    game['cursor_1'] = 0
    game['cursor_spot'] = 0
    game['options'] = {
        "Human" : ["Warrior", "Mage", "Archer", "Thief", "Farmer", "Begger"],
        "Dwarf" : ['Warrior', "King"],
        "Elf" : ['Mystic', 'Assassin'],
        "Goblin" : ['Wanderer']
    }

def load_gamestart(game, race, clss):
    game['option'] = -1
    game['game_state'] = GameStates.PLAYER_TURN
    game['room_max_size'] = 10
    game['room_min_size'] = 5
    game['max_rooms'] = 100 # 30
    game['fov_recompute'] = True
    game['player'] = Entity(int(game['screen_width'] / 2), int(game['screen_height'] / 2), '@', libtcod.white, race+" "+clss, race, inventory=Inventory(gold=20))
    game['camera_x'] = game['player'].x
    game['camera_y'] = game['player'].y
    npc = Entity(int(game['screen_width'] / 2 - 5), int(game['screen_height'] / 2), '@', libtcod.red, "Human Merchant", "Human", blocks = True, ai=BasicMerchant())
    npc2 = Entity(int(game['screen_width'] / 2 + 5), int(game['screen_height'] / 2 + 5), '@', libtcod.green, "Lost Elf", "Elf", blocks = True, ai=Wander(), traits=[], inventory=Inventory(gold=-1))
    game['entities'] = [game['player'], npc, npc2]
    game['items'] = []
    game['game_map'] = GameMap(game['map_width'], game['map_height'])
    game['game_map'].make_map(game['max_rooms'], game['room_min_size'], game['room_max_size'], game['map_width'], game['map_height'], game['player'], game['entities'], 1, 1, game)
    game['fov_map'] = initialize_fov(game['game_map'])
    game['slot_names'] = ['Head', "Neck", "Chest", "Back", "Left Arm", "Right Arm", "Left Hand", "Right Hand", "Belt", "Legs", "Left Foot", "Right Foot"]

    for i in range(10):
        new_item = make_item(sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1)[0])
        place_item(new_item, game, game['player'].x+2, game['player'].y+2)
        
    
def load_ground_menu(game):
    game['game_state'] = GameStates.GROUND_MENU
    game['cursor'] = 0
    game['option'] = 0

def load_equipment_menu(game):
    game['game_state'] = GameStates.EQUIPMENT_MENU
    game['cursor_0'] = 0
    game['cursor_1'] = 0
    game['cursor_spot'] = 0
    game['option'] = 1

def load_inventory_menu(game):
    game['game_state'] = GameStates.INVENTORY_MENU
    game['cursor_0'] = 0
    game['cursor_1'] = 0
    game['cursor_2'] = 0
    game['cursor_spot'] = 0
    game['option'] = 2