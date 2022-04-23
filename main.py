import libtcodpy as libtcod
from time import sleep
from bundled.game_messages import Message
from bundled.item_loader import place_item, remove_item_from_map
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from helper_funcs import gear_lookup, get_items_at_loc
from input_handlers import handle_charselect_keys, handle_equipment_menu_keys, handle_ground_menu_keys, handle_mainmenu_keys, handle_playerturn_keys
from map_objects.game_map import GameMap
from menus import equipment_menu, ground_menu, main_menu, char_select_menu, menu_strip
from render_functions import clear_all, render_all, render_animations, render_base_screen
from game_states import GameStates
from animations import animation
from unit_components.ai import BasicMerchant, Wander
from unit_components.damage import Damage
from unit_components.inventory import Inventory
from unit_components.item import Item
from unit_components.stat_mod import trait
from pprint import pprint
from time import sleep
from bundled.loaders import load_charselect, load_equipment_menu, load_gamestart, load_ground_menu, load_inventory_menu, load_preamble, load_mainmenu
VERSION = "0.0.12"
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
                    game['message_log'].add_message(Message("You begin your journey as a {} {}".format(
                        list(game['options'].keys())[game['cursor_0']],
                        game['options'][list(game['options'].keys())[game['cursor_0']]][game['cursor_1']]
                    )))
                    load_gamestart(
                        game, 
                        race=list(game['options'].keys())[game['cursor_0']],
                        clss=game['options'][list(game['options'].keys())[game['cursor_0']]][game['cursor_1']]
                    )
        
        elif game['game_state'] == GameStates.EQUIPMENT_MENU:
            
            render_base_screen(game)
            equipment_menu(game['con'], game)
            libtcod.console_flush()
            clear_all(game['con'], game['entities'], game)

            action = handle_equipment_menu_keys(game['key'])

            move = action.get('move')
            select = action.get('select')
            exit = action.get('exit')
            back = action.get('back')
            drop = action.get('drop')
            jump = action.get('jump')
            tab = action.get('tab')

            if move:
                if game['cursor_spot'] == 0:
                    game['cursor_0'] = ( game['cursor_0'] + move ) % len(game['slot_names'])
                elif game['cursor_spot'] == 1:
                    game['cursor_1'] = ( game['cursor_1'] + move ) % len(game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])])
            if tab:
                game['cursor_tab'] = ( game['cursor_tab'] + 1 ) % game['cursor_tab_options']
            if jump:
                if game['cursor_spot'] == 0:
                    if jump == 'down':
                        game['cursor_0'] = len(game['slot_names'])-1
                    elif jump == 'up':
                        game['cursor_0'] = 0
                if game['cursor_spot'] == 1:
                    itms = len(game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]) 
                    p_size = len(game['slot_names'])
                    if jump == 'down':
                        if itms > p_size:
                            if game['cursor_1'] == itms-1:
                                game['cursor_1'] = p_size-1
                            else:
                                if game['cursor_1'] + p_size > itms-1:
                                    game['cursor_1'] = itms-1
                                else:                        
                                    game['cursor_1'] = (game['cursor_1'] + p_size) % itms
                        else:
                            game['cursor_1'] = itms-1
                    if jump == 'up':
                        if itms > p_size:
                            if game['cursor_1'] < p_size:
                                if game['cursor_1'] == 0:
                                    game['cursor_1'] = p_size - game['cursor_1']
                                else:
                                    game['cursor_1'] = 0
                            else:
                                game['cursor_1'] -= p_size
                        else:
                            game['cursor_1'] = 0


                    
                    
            if select:
                if game['cursor_spot'] == 0:
                    if len(game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]) > 0:
                        game['cursor_spot'] = 1
                elif game['cursor_spot'] == 1:
                    selected_item = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])][game['cursor_1']]
                    game['player'].inventory.equip_item(selected_item, position = game['slot_names'][game['cursor_0']])
                    game['message_log'].add_message(Message("You equip {}".format(selected_item.name)))
                    game['cursor_spot'] = 0
                    game['cursor_1'] = 0
            if back:
                if game['cursor_spot'] == 1:
                    game['cursor_spot'] = 0
                    game['cursor_1'] = 0
            if exit:
                game['game_state'] = GameStates.PLAYER_TURN
                game['option'] = -1
            if drop:
                if game['cursor_spot'] == 0:
                    # unequip to bag
                    if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                        game['player'].inventory.unequip_item(game['slot_names'][game['cursor_0']])
                elif game['cursor_spot'] == 1:
                    # drop
                    selected_item = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])][game['cursor_1']].copy_self()
                    place_item(selected_item, game, game['player'].x, game['player'].y)
                    game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])][game['cursor_1']].quantity -= 1
                    if game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])][game['cursor_1']].quantity <=0:
                        game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])].remove(
                            game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])][game['cursor_1']]
                        )
                    game['cursor_1'] -= 1
                    if game['cursor_1'] < 0:
                        game['cursor_1'] = 0
                    if len(game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]) <= 0:
                        game['cursor_spot'] = 0
            

        elif game['game_state'] == GameStates.GROUND_MENU:
            items = get_items_at_loc(game, game['player'].x, game['player'].y)
            render_base_screen(game)
            ground_menu(game['con'], game, items)
            libtcod.console_flush()
            clear_all(game['con'], game['entities'], game)

            action = handle_ground_menu_keys(game['key'])

            move = action.get('move')
            select = action.get('select')
            exit = action.get('exit')
            jump = action.get('jump')

            if move and len(items) > 0:
                game['cursor'] = ( game['cursor'] + move ) % len(items)
            if exit:
                game['game_state'] = GameStates.PLAYER_TURN
                game['option'] = -1
            if select and len(items) > 0:
                Selected = items[game['cursor']]
                game['player'].inventory.get_item(Selected)
                remove_item_from_map(Selected, game)
                if game['cursor']+1 >= len(items):
                    game['cursor'] -= 1
            if jump:
                itms = len(items) 
                p_size = 13
                if jump == 'down':
                    if itms > p_size:
                        if game['cursor'] == itms-1:
                            game['cursor'] = p_size-1
                        else:
                            if game['cursor'] + p_size > itms-1:
                                game['cursor'] = itms-1
                            else:                        
                                game['cursor'] = (game['cursor'] + p_size) % itms
                    else:
                        game['cursor'] = itms-1
                if jump == 'up':
                    if itms > p_size:
                        if game['cursor'] < p_size:
                            if game['cursor'] == 0:
                                game['cursor'] = p_size - game['cursor']
                            else:
                                game['cursor'] = 0
                        else:
                            game['cursor'] -= p_size
                    else:
                        game['cursor'] = 0

        elif game['game_state'] == GameStates.MAIN_MENU:
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
            render_base_screen(game)
            libtcod.console_flush()
            clear_all(game['con'], game['entities'], game)

            if game['game_state'] == GameStates.PLAYER_TURN:
                action = handle_playerturn_keys(game['key'])

            move = action.get('move')
            exit = action.get('exit')
            fullscreen = action.get('fullscreen')
            ground_menu_opened = action.get('ground_menu_opened')
            equipment_menu_opened = action.get('equipment_menu_opened')
            inventory_menu_opened = action.get('inventory_menu_opened')

            if ground_menu_opened:
                load_ground_menu(game)
            if equipment_menu_opened:
                load_equipment_menu(game)
            if inventory_menu_opened:
                load_inventory_menu(game)
            if move and game['game_state'] == GameStates.PLAYER_TURN:
                dx, dy = move
                destination_x = game['player'].x + dx
                destination_y = game['player'].y + dy
                if not game['game_map'].is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(game['entities'], destination_x, destination_y)
                    
                    game['fov_recompute'] = True
                    if target:
                        game['message_log'].add_message(Message('You kick the ' + target.name + ' in the shins, much to its annoyance!'))
                    else:
                        game['player'].move(dx, dy)
                else:
                    game['message_log'].add_message(Message('You kick the wall'))
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