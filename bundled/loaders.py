
from random import sample
from bundled.game_messages import MessageLog
from bundled.item_loader import ascii_loader, make_item, place_item
from entity import Entity
from fov_functions import initialize_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from unit_components.ai import BasicMerchant, Wander
from unit_components.inventory import Inventory
import tcod as libtcod

def load_preamble(game, VERSION):
    # Size of window
    game['screen_width'] = 57
    game['screen_height'] = 31

    # Map size( Can change )
    game['map_width'] = 150#80
    game['map_height'] = 90#44

    # units are in map units
    game['info_panel_height'] = game['screen_height']
    game['info_panel_width'] = 15

    game['bar_width'] = 40
    game['panel_height'] = 15 # MUST BE ODD
    game['panel_width'] = game['screen_width'] - game['info_panel_width']
    game['panel_y'] = game['screen_height'] - game['panel_height']

    
    # Camera Size 
    game['camera_width'] = game['screen_width'] - game['info_panel_width']
    game['camera_height'] = game['screen_height'] - int((game['panel_height']+4)/2)

    
    game['tileset_text'] = libtcod.tileset.load_tilesheet("./tilesets/arial10x10.png", 32, 8, libtcod.tileset.CHARMAP_TCOD)
    game['tileset_title'] = libtcod.tileset.load_tilesheet("./tilesets/large48x48.png", 16, 16, libtcod.tileset.CHARMAP_CP437)
    game['tileset_map'] = libtcod.tileset.load_tilesheet("./tilesets/test32x32.png", 16, 16, libtcod.tileset.CHARMAP_CP437)


    game['message_x'] = game['bar_width'] + 2
    # Convert to text font width
    # print(game['screen_width']*game['tileset_map'].tile_width)
    # print(game['tileset_text'].tile_width)
    game['message_width'] = 1+int(game['screen_width']*game['tileset_map'].tile_width/game['tileset_text'].tile_width)-2-int(game['tileset_map'].tile_width*game['info_panel_width']/game['tileset_text'].tile_width) #game['screen_width'] -2  # - game['bar_width'] - 2
    game['message_height'] = game['panel_height']-1
    game['message_log'] = MessageLog(game['message_x'], game['message_width']-3, game['message_height']-2)

    # Cleared after every round
    game['console_base'] = libtcod.Console(game['screen_width'], game['screen_height'])
    game['sdl_window'] = libtcod.sdl.video.new_window(
        game['console_base'].width * game['tileset_map'].tile_width,
        game['console_base'].height * game['tileset_map'].tile_height,
        flags=libtcod.lib.SDL_WINDOW_RESIZABLE,
    )
    game['sdl_renderer'] = libtcod.sdl.render.new_renderer(game['sdl_window'], target_textures = True)

    game['panel'] = libtcod.console_new(game['screen_width'], game['panel_height'])
    game['atlas_text'] = libtcod.render.SDLTilesetAtlas(game['sdl_renderer'], game['tileset_text'])
    game['atlas_title'] = libtcod.render.SDLTilesetAtlas(game['sdl_renderer'], game['tileset_title'])
    game['atlas_map'] = libtcod.render.SDLTilesetAtlas(game['sdl_renderer'], game['tileset_map'])

    game['console_renderer_text'] = libtcod.render.SDLConsoleRender(game['atlas_text'])
    game['console_renderer_title'] = libtcod.render.SDLConsoleRender(game['atlas_title'])
    game['console_renderer_map'] = libtcod.render.SDLConsoleRender(game['atlas_map'])
    
    
    
    game['fov_algorithm'] = 4
    game['fov_light_walls'] = True
    #libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #libtcod.console_set_custom_font('Talryth_square_15x15.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    #libtcod.console_set_custom_font('drd15x15.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    #libtcod.console_init_root(game['screen_width'], game['screen_height'], 'Dragons are Dungeons 3: {}'.format(VERSION), False)
    #game['con'] = libtcod.console_new(game['screen_width'], game['screen_height'])
    game['key'] = libtcod.Key()
    game['mouse'] = libtcod.Mouse()

    game['TILES'] = ascii_loader()



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
    game['player'] = Entity(int(game['screen_width'] / 2), int(game['screen_height'] / 2), game['TILES']['PLAYER']['CHAR'], game['TILES']['PLAYER']['COLOR'], race+" "+clss, race, clss, inventory=Inventory(gold=20))
    game['camera_x'] = game['player'].x
    game['camera_y'] = game['player'].y

    npc = Entity(int(game['screen_width'] / 2 - 5), int(game['screen_height'] / 2), game['TILES']['NPC']['CHAR'], game['TILES']['NPC']['COLOR'], "Human Merchant", "Human", blocks = True, ai=BasicMerchant())
    npc2 = Entity(int(game['screen_width'] / 2 + 5), int(game['screen_height'] / 2 + 5), game['TILES']['NPC']['CHAR'], game['TILES']['NPC']['COLOR'], "Lost Elf", "Elf", blocks = True, ai=Wander(), traits=[], inventory=Inventory(gold=-1))
    game['entities'] = [game['player'], npc, npc2]
    for y in range(10):
        for i in range(50):
            samp = sample([1, 2, 3, 4, 5], 1)[0]
            if samp == 1:
                newpc = Entity(5+y, i+10, game['TILES']['NPC']['CHAR'], game['TILES']['NPC']['COLOR'], "Human Merchant", "Human", blocks = True, ai=BasicMerchant())
            elif samp == 2:
                newpc = Entity(5+y, i+10, game['TILES']['NPC']['CHAR'], libtcod.darkest_green, "Orc Warrior", "Orc", blocks = True, ai=BasicMerchant())
            elif samp == 3:
                newpc = Entity(5+y, i+10, game['TILES']['NPC']['CHAR'], libtcod.green, "Goblin Spy", "Goblin", blocks = True, ai=BasicMerchant())
            elif samp == 4:
                newpc = Entity(5+y, i+10, game['TILES']['NPC']['CHAR'], game['TILES']['NPC']['COLOR'], "Stupid Elf", "Elf", blocks = True, ai=BasicMerchant())
            elif samp == 5:
                newpc = Entity(5+y, i+10, game['TILES']['NPC']['CHAR'], libtcod.dark_gray, "Dwarf Digger", "Dwarf", blocks = True, ai=BasicMerchant())
            game['entities'].append(newpc)
    game['items'] = []
    game['item_display_page'] = 0
    game['item_display_sort'] = 0 # ['value', 'alphabetic', 'dist']
    game['entity_display_page'] = 0
    game['entity_display_sort'] = 0
    game['game_map'] = GameMap(game['map_width'], game['map_height'])
    game['game_map'].make_map(game['max_rooms'], game['room_min_size'], game['room_max_size'], game['map_width'], game['map_height'], game['player'], game['entities'], 1, 1, game)
    game['fov_map'] = initialize_fov(game['game_map'])
    game['slot_names'] = ['Head', "Neck", "Chest", "Back", "Left Arm", "Right Arm", "Left Hand", "Right Hand", "Left Ring", "Right Ring", "Belt", "Legs", "Left Foot", "Right Foot"]
    #game['message_log'] = MessageLog(message_x, message_width, message_height)
    for i in range(10):
        new_item = make_item(sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1)[0], game)
        place_item(new_item, game, game['player'].x+2, game['player'].y+2)
    for i in range(50):
        new_item = make_item(sample([1, 2], 1)[0], game)
        place_item(new_item, game, game['player'].x+2, game['player'].y+1)
        
    
def load_ground_menu(game):
    
    game['game_state'] = GameStates.GROUND_MENU
    game['cursor'] = 0
    game['option'] = 0

def load_equipment_menu(game):
    game['game_state'] = GameStates.EQUIPMENT_MENU
    game['cursor_0'] = 0
    game['cursor_1'] = 0
    game['cursor_spot'] = 0
    game['cursor_tab'] = 0
    game['cursor_tab_options'] = 3
    game['option'] = 1

def load_inventory_menu(game):
    game['game_state'] = GameStates.INVENTORY_MENU
    game['cursor_0'] = 0
    game['cursor_1'] = 0
    game['cursor_2'] = 0
    game['cursor_spot'] = 0
    game['option'] = 2