import libtcodpy as libtcod

from fov_functions import recompute_fov
from menus import menu_strip

def render_base_screen(game):

    if game['fov_recompute']:
        recompute_fov(game['fov_map'], game['player'].x, game['player'].y, game['player'].stats.sight, game['fov_light_walls'], game['fov_algorithm'])

    render_all(game['con'], game['player'], game['entities'], game['game_map'], game['fov_map'], game['fov_recompute'],
            game['screen_width'], game['screen_height'], game['camera_width'], game['camera_height'], game)

    game['fov_recompute'] = False

    menu_strip(game['con'], game)

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

def render_all(con, player, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, camera_width, camera_height, game):
    move_camera(game['player'].x, game['player'].y, game)
    if fov_recompute:
    # Draw all the tiles in the game map
        for y in range(game['camera_height']):
            for x in range(game['camera_width']):
                (map_x, map_y) = (game['camera_x'] + x, game['camera_y'] + y)
                visible = libtcod.map_is_in_fov(fov_map, map_x, map_y)
                wall = game_map.tiles[map_x][map_y].block_sight

                

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Visible"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Visible"), libtcod.BKGND_SET)
                    game_map.tiles[map_x][map_y].explored = True
                    game_map.tiles[map_x][map_y].last_seen = 0

                elif game_map.tiles[map_x][map_y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Explored"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Explored"), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET)
                
                if game_map.tiles[map_x][map_y].explored and not visible:
                    if game_map.tiles[map_x][map_y].step(player):
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Unseen"), libtcod.BKGND_SET)

    # Draw all items
    for item in game['items']:
        draw_item(con, item, fov_map, game)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map, game)

    # Test
    #libtcod.console_put_char(con, game['player'].x+1, game['player'].y, 180, libtcod.BKGND_NONE)
    # Print the game messages, one line at a time
   

    libtcod.console_blit(con, 0, 0, camera_width, camera_height, 20, 0,  0)

    libtcod.console_set_default_background(game['panel'], libtcod.black)
    libtcod.console_clear(game['panel'])

    y = 1
    for message in game['message_log'].messages:
        libtcod.console_set_default_foreground(game['panel'], message.color)
        libtcod.console_print_ex(game['panel'], game['message_log'].x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(game['panel'], 1, 1, game['bar_width'], 'HP', game['player'].stats.hp, game['player'].stats.max_hp,
               libtcod.lighter_red, libtcod.darker_red, game)
    render_bar(game['panel'], 1, 3, game['bar_width'], 'MP', game['player'].stats.mp, game['player'].stats.max_mp,
               libtcod.lighter_blue, libtcod.darker_blue, game)

    libtcod.console_blit(game['panel'], 0, 0, screen_width, game['panel_height'], 0, 0, game['panel_y'])
    #libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

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

def draw_entity(con, entity, fov_map, game):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        (x, y) = to_camera_coordinates(entity.x, entity.y, game)
        if x is not None:
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)

def draw_item(con, item, fov_map, game):
    if libtcod.map_is_in_fov(fov_map, item.x, item.y):
        (x, y) = to_camera_coordinates(item.x, item.y, game)
        if x is not None:
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, item.color)
            libtcod.console_put_char(con, x, y, item.char, libtcod.BKGND_NONE)


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
