import time
import libtcodpy as libtcod

from fov_functions import recompute_fov
from menus import menu_strip

def render_base_screen(game, present = True):
    #strip_console = libtcod.Console(int(game['screen_width']*game['tileset_map'].tile_width/game['tileset_text'].tile_width), 1)
    #time.sleep(.1) 
    if game['fov_recompute']:
        recompute_fov(game['fov_map'], game['player'].x, game['player'].y, game['player'].stats.sight, game['fov_light_walls'], game['fov_algorithm'])
    render_all(game)
    # game['sdl_renderer'].present()
    
    
    

    menu_strip(game)
    # game['sdl_renderer'].copy(
    #     game['console_renderer_map'].render(map_console),
    #     dest = (
    #         0, 0,
    #         map_console.width*game['tileset_map'].tile_width,
    #         map_console.height*game['tileset_map'].tile_height
    # ))
    
    
    if present:
        game['sdl_renderer'].present()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, game):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(game):
    # if "map_console" in game.keys():
    #     map_console = game['map_console']
    # else:
    map_console = libtcod.Console(game['screen_width'], game['screen_height'])
    #    game['map_console'] = map_console
    move_camera(game['player'].x, game['player'].y, game)
    #if game['fov_recompute']:
    if True:
    # Draw all the tiles in the game map
        for y in range(game['camera_height']):
            for x in range(game['camera_width']):
                (map_x, map_y) = (game['camera_x'] + x, game['camera_y'] + y)
                visible = libtcod.map_is_in_fov(game['fov_map'], map_x, map_y)
                wall = game['game_map'].tiles[map_x][map_y].block_sight
                if visible:
                    map_console.print(x, y, game['game_map'].tiles[map_x][map_y].char, game['game_map'].tiles[map_x][map_y].get_fg_color("Visible"), game['game_map'].tiles[map_x][map_y].get_bg_color("Visible"))
                    # if wall:
                    #     libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Visible"), libtcod.BKGND_SET)
                    # else:
                    #     libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Visible"), libtcod.BKGND_SET)
                    game['game_map'].tiles[map_x][map_y].explored = True
                    game['game_map'].tiles[map_x][map_y].last_seen = 0

                elif game['game_map'].tiles[map_x][map_y].explored:
                    map_console.print(x, y, game['game_map'].tiles[map_x][map_y].char, game['game_map'].tiles[map_x][map_y].get_fg_color("Explored"), game['game_map'].tiles[map_x][map_y].get_bg_color("Explored"))
                    # if wall:
                    #     libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Explored"), libtcod.BKGND_SET)
                    # else:
                    #     libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Explored"), libtcod.BKGND_SET)
                #else:
                    #map_console.print(x, y, " ", libtcod.black, libtcod.BKGND_SET)
                    #libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET)
                
                # TODO in case something is glowing in teh dark
                # if game_map.tiles[map_x][map_y].explored and not visible:
                #     if game_map.tiles[map_x][map_y].step(player):
                #         libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Unseen"), libtcod.BKGND_SET)
    
    
    # Draw all items
    for item in game['items']:
        draw_item(item, game['fov_map'], game, map_console)

    # Draw all entities in the list
    for entity in game['entities']:
        draw_entity(entity, game['fov_map'], game, map_console)

    # Test
    #libtcod.console_put_char(con, game['player'].x+1, game['player'].y, 180, libtcod.BKGND_NONE)
    # Print the game messages, one line at a time
   

    # libtcod.console_blit(con, 0, 0, camera_width, camera_height, 20, 0,  0)

    # libtcod.console_set_default_background(game['panel'], libtcod.black)
    # libtcod.console_clear(game['panel'])
    game['fov_recompute'] = False
    game['sdl_renderer'].copy(
        game['console_renderer_map'].render(map_console),
        dest = (
            0, 0,
            map_console.width*game['tileset_map'].tile_width,
            map_console.height*game['tileset_map'].tile_height
    ))
    #TODO REACTIVATE
    # y = 1
    # for message in game['message_log'].messages:
    #     libtcod.console_set_default_foreground(game['panel'], message.color)
    #     libtcod.console_print_ex(game['panel'], game['message_log'].x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
    #     y += 1

    # render_bar(game['panel'], 1, 1, game['bar_width'], 'HP', game['player'].stats.hp, game['player'].stats.max_hp,
    #            libtcod.lighter_red, libtcod.darker_red, game)
    # render_bar(game['panel'], 1, 3, game['bar_width'], 'MP', game['player'].stats.mp, game['player'].stats.max_mp,
    #            libtcod.lighter_blue, libtcod.darker_blue, game)

    # libtcod.console_blit(game['panel'], 0, 0, screen_width, game['panel_height'], 0, 0, game['panel_y'])

    
    #game['sdl_renderer'].present()
    

def move_camera(target_x, target_y, game):
	#new camera coordinates (top-left corner of the screen relative to the map)
    x = target_x - int(game['camera_width'] / 2)  #coordinates so that the target is at the center of the screen
    y = target_y - int(game['camera_height'] / 2)
	#make sure the camera doesn't see outside the map
    if x < 0: 
        x = 0
    if y < 0: 
        y = 0
    if x > game['map_width'] - game['camera_width'] - 1: 
        x = game['map_width'] - game['camera_width'] - 1
    if y > game['map_height'] - game['camera_height'] - 1: 
        y = game['map_height'] - game['camera_height'] - 1
 
    if x != game['camera_x'] or y != game['camera_y']: 
        game['fov_recompute'] = True
    (game['camera_x'], game['camera_y']) = (x, y)
 
def to_camera_coordinates(x, y, game):
	#convert coordinates on the map to coordinates on the screen
	(x, y) = (x - game['camera_x'], y - game['camera_y'])
 
	if (x < 0 or y < 0 or x >= game['camera_width'] or y >= game['camera_height']):
		return (None, None)  #if it's outside the view, return nothing
 
	return (x, y)

def clear_all(con, entities, game):
    for entity in entities:
        clear_entity(con, entity, game)
    for item in game['items']:
        clear_item(con, item, game)

def draw_entity(entity, fov_map, game, map_console):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        (x, y) = to_camera_coordinates(entity.x, entity.y, game)
        if x is not None:
            #set the color and then draw the character that represents this object at its position
            #libtcod.Console(1, 2).print(x, y, str(entity.char)
            map_console.print(x, y, str(entity.char), entity.color)
            # libtcod.console_set_default_foreground(con, entity.color)
            # libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)

def draw_item(item, fov_map, game, map_console):
    if libtcod.map_is_in_fov(fov_map, item.x, item.y):
        (x, y) = to_camera_coordinates(item.x, item.y, game)
        if x is not None:
            #set the color and then draw the character that represents this object at its position
            map_console.print(x, y, str(item.char), item.color)
            #libtcod.console_set_default_foreground(con, item.color)
            #libtcod.console_put_char(con, x, y, item.char, libtcod.BKGND_NONE)


def render_animations(con, animations, fov_map):
    for ani in animations:
        tle = ani.next_step()
        if libtcod.map_is_in_fov(fov_map, tle.x, tle.y):
            libtcod.console_set_char_background(con, tle.x, tle.y, tle.get_color("Visible"), libtcod.BKGND_SET)
        

def clear_entity(con, entity, game):
    (x, y) = to_camera_coordinates(entity.x, entity.y, game)
    if x is not None:
        # erase the character that represents this object
        libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)

def clear_item(con, item, game):
    (x, y) = to_camera_coordinates(item.x, item.y, game)
    if x is not None:
        # erase the character that represents this object
        libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
