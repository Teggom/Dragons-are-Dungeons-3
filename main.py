import libtcodpy as libtcod
from time import sleep
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_charselect_keys, handle_mainmenu_keys, handle_playerturn_keys
from map_objects.game_map import GameMap
from menus import main_menu, char_select_menu
from render_functions import clear_all, render_all, render_animations
from game_states import GameStates
from animations import animation
from unit_components.ai import BasicMerchant, Wander
from unit_components.damage import Damage
from unit_components.inventory import Inventory
from unit_components.item import Item
from unit_components.stat_mod import trait
from pprint import pprint
from bundled.loaders import load_charselect, load_gamestart, load_preamble, load_mainmenu
VERSION = "0.0.7"
game = {}

def main():
    load_preamble(game, VERSION)
    load_mainmenu(game)
    # Some variables for the rooms in the map


    #game_state = GameStates.PLAYER_TURN
    # blindness = trait("Blindness", sight=-40)
    # supervision = trait("Supervision", sight=40)
    # photomem = trait("Photographic Memory", memory=30)
    # dory = trait("Dory", memory=-30)

    
    #animations = []
    
    while not libtcod.console_is_window_closed():
        action = {}
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, game['key'], game['mouse'])
        
        if game['game_state'] == GameStates.CHARACTER_SELECT:
            char_select_menu(game['con'], game)
            libtcod.console_flush()
            action = handle_charselect_keys(game['key'])

            move = action.get('move')
            exit = action.get('exit')
            select = action.get('select')
            back = action.get('back')
            if move:
                if game['cursor_spot'] == 0:
                    game['cursor_0'] = ( game['cursor_0'] + move ) % len(game['options'].keys())
                else:
                    game['cursor_1'] = ( game['cursor_1'] + move ) % len(game['options'][list(game['options'].keys())[game['cursor_0']]])
            if exit:
                load_mainmenu(game)
            if back:
                if game['cursor_spot'] == 0:
                    load_mainmenu()
                else:
                    game['cursor_1'] = 0
                    game['cursor_spot'] = 0
            if select:
                if game['cursor_spot'] == 0:
                    game['cursor_spot'] = 1
                else:
                    load_gamestart(
                        game, 
                        race=list(game['options'].keys())[game['cursor_0']],
                        clss=game['options'][list(game['options'].keys())[game['cursor_0']]][game['cursor_1']]
                    )
            

        if game['game_state'] == GameStates.MAIN_MENU:
            # RENDER MENU
            main_menu(game['con'], 'menu_background.png', game)
            libtcod.console_flush()
            action = handle_mainmenu_keys(game['key'])

            move = action.get('move')
            exit = action.get('exit')
            select = action.get('select')

            if move:
                game['cursor'] = ( game['cursor'] + move ) % len(game['options'])
            if exit:
                return True
            if select:
                SELECTED = game['options'][game['cursor']]
                if SELECTED == 'New Game':
                    load_charselect(game)
                # OPTIONS
                # CREDITS
                if SELECTED == 'Exit':
                    return True

        elif game['game_state'] == GameStates.PLAYER_TURN:
            if game['fov_recompute']:
                recompute_fov(game['fov_map'], game['player'].x, game['player'].y, game['player'].stats.sight, game['fov_light_walls'], game['fov_algorithm'])
            render_all(game['con'], game['player'], game['entities'], game['game_map'], game['fov_map'], game['fov_recompute'],
                 game['screen_width'], game['screen_height'], game['camera_width'], game['camera_height'])

            game['fov_recompute'] = False

            libtcod.console_flush()

            clear_all(game['con'], game['entities'])

            if game['game_state'] == GameStates.PLAYER_TURN:
                action = handle_playerturn_keys(game['key'])

            move = action.get('move')
            exit = action.get('exit')
            fullscreen = action.get('fullscreen')

            if move and game['game_state'] == GameStates.PLAYER_TURN:
                dx, dy = move
                destination_x = game['player'].x + dx
                destination_y = game['player'].y + dy
                if not game['game_map'].is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(game['entities'], destination_x, destination_y)
                    
                    game['fov_recompute'] = True
                    if target:
                        print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                    else:
                        game['player'].move(dx, dy)
                game['player'].step()
                game['game_state'] = GameStates.ENEMY_TURN

            if game['game_state'] == GameStates.ENEMY_TURN:
                for entity in game['entities']:
                    if not entity.dead:
                        if entity.ai:
                            entity.ai.take_turn(game['player'], game['fov_map'], game['game_map'], game['entities'])
                            entity.step()
                game['game_state'] = GameStates.PLAYER_TURN


            if exit:
                load_mainmenu(game)

            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
     main()