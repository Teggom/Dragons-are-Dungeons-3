from audioop import reverse
import math
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
def render_bar(console, x, y, width, value, maximum, b_fg, b_bg, percent = False, t_fg = libtcod.black):
    bar_width = int(float(value) / maximum * width)
    if percent:
        to_print = str(round(100*value/maximum, 2)) + " %"
    else:
        to_print = str(value) + "/" + str(maximum)
    
    console.print(x, y, " "*width, b_bg, b_bg, libtcod.BKGND_SET, libtcod.LEFT)
    console.print(x, y, " "*bar_width, b_fg, b_fg, libtcod.BKGND_SET, libtcod.LEFT)
    console.print(x + int(width/2), y, to_print, t_fg, libtcod.black, libtcod.BKGND_NONE, libtcod.CENTER)
    
    
def render_bar2(panel, x, y, total_width, name, value, maximum, bar_color, back_color, game):
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
    map_console = libtcod.Console(game['camera_width'], game['camera_height'])
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
                # else:
                #     map_console.print(x, y, " ", libtcod.black, libtcod.black, libtcod.BKGND_SET)
                    #libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET)
                
                # TODO in case something is glowing in teh dark
                # if game_map.tiles[map_x][map_y].explored and not visible:
                #     if game_map.tiles[map_x][map_y].step(player):
                #         libtcod.console_set_char_background(con, x, y, game_map.tiles[map_x][map_y].get_color("Unseen"), libtcod.BKGND_SET)
    
    to_display_items = []
    to_display_entities = []
    # Draw all items
    for item in game['items']:
        if draw_item(item, game['fov_map'], game, map_console):
            to_display_items.append(item)

    # Draw all entities in the list
    for entity in game['entities']:
        if draw_entity(entity, game['fov_map'], game, map_console):
            if entity != game['player']:
                to_display_entities.append(entity)

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
            0, 16,
            map_console.width*game['tileset_map'].tile_width,
            (map_console.height+1)*game['tileset_map'].tile_height
    ))

    message_console = libtcod.Console(game['message_width'], game['message_height'])
    message_console.print_frame(0, 0, game['message_width'], game['message_height'], "Messages")
    #message_console.print(1, 1, '-'*100, libtcod.white, libtcod.blue, alignment=libtcod.CENTER)
    
    y = 1
    for i, message in enumerate(game['message_log'].messages):
        message_console.print(2, y, message.text, message.color, libtcod.black, libtcod.BKGND_NONE, libtcod.LEFT)
        y += 1
        #TODO only show selected verbosity
    
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(message_console),
        dest = (
            10,
            map_console.height*game['tileset_map'].tile_height+game['tileset_text'].tile_height*3,
            game['message_width']*game['tileset_text'].tile_width,
            (game['message_height'])*game['tileset_text'].tile_height
    ))


    # y = 0
    # for message in game['message_log'].messages:
    #     libtcod.console_set_default_foreground(game['panel'], message.color)
    #     libtcod.console_print_ex(game['panel'], game['message_log'].x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
    #     y += 1


    info_panel_width = int(game['info_panel_width']*game['tileset_map'].tile_width/game['tileset_text'].tile_width)-1
    info_panel_height = int(game['info_panel_height']*game['tileset_map'].tile_height/game['tileset_text'].tile_height)-2
    info_panel_console = libtcod.Console(info_panel_width, info_panel_height)
    # print('-')
    # print(game['screen_width']*game['tileset_map'].tile_width)
    # print(info_panel_width*game['tileset_text'].tile_width)
    # print(game['info_panel_width'])
    # print(game['info_panel_height']*game['tileset_map'].tile_height)
    # print(game['screen_height']*game['tileset_map'].tile_height)
    # print((info_panel_width, info_panel_height))

    pref = game['player'].stats


    info_panel_console.print_frame(0, 0, info_panel_width, info_panel_height, "Here's what you Know")
    
    # TOP STATS
    fg, bg = (libtcod.gray, libtcod.black)
    info_panel_console.print(int(info_panel_width/2)-1, 2, game['player'].name, libtcod.lighter_gray, bg, libtcod.BKGND_NONE, libtcod.CENTER)
    info_panel_console.print(int(info_panel_width/2)-1, 3, game['player'].race, fg, bg, libtcod.BKGND_NONE, libtcod.CENTER)
    info_panel_console.print(int(info_panel_width/2)-1, 4, game['player'].clss, fg, bg, libtcod.BKGND_NONE, libtcod.CENTER)
    if game['player'].inventory.wearing['Right Hand']:
        rh = game['player'].inventory.wearing['Right Hand'].t_name
        rh_fg = libtcod.lighter_gray
    else:
        rh = "Nothing"
        rh_fg = libtcod.darkest_gray
    if game['player'].inventory.wearing['Left Hand']:
        lh = game['player'].inventory.wearing['Left Hand'].t_name
        lh_fg = libtcod.lighter_gray
    else:
        if game['player'].inventory.wearing['Right Hand'] and game['player'].inventory.wearing['Right Hand'].twohand:
            lh = rh
            lh_fg = libtcod.darker_gray
        else:
            lh = "Nothing"
            lh_fg = libtcod.darkest_gray
    info_panel_console.print(int(info_panel_width/3)-1, 6, "Right Hand: ", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
    info_panel_console.print(int(info_panel_width/3), 6, rh, rh_fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
    info_panel_console.print(int(info_panel_width/3)-1, 7, "Left Hand: ", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
    info_panel_console.print(int(info_panel_width/3), 7, lh, lh_fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
    info_panel_console.print(int(info_panel_width/3)-1, 9, "Base Noise: ", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
    info_panel_console.print(int(info_panel_width/3), 9, str(game['player'].stats.noise), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
    info_panel_console.print(int(info_panel_width/3)-1, 10, "Gear Worth: ", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
    info_panel_console.print(int(info_panel_width/3), 10, str(game['player'].inventory.gear_worth), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
    info_panel_console.print(int(info_panel_width/3)-1, 11, "Bag Worth: ", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
    info_panel_console.print(int(info_panel_width/3), 11, str(game['player'].inventory.bag_worth), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
    
    info_panel_console.print(4, 13, "HP:", fg, bg, libtcod.BKGND_SET, libtcod.RIGHT)
    render_bar(info_panel_console, 5, 13, info_panel_width-7, game['player'].stats.hp, game['player'].stats.max_hp, libtcod.red, libtcod.darker_red)
    info_panel_console.print(4, 14, "MP:", fg, bg, libtcod.BKGND_SET, libtcod.RIGHT)
    render_bar(info_panel_console, 5, 14, info_panel_width-7, game['player'].stats.mp, game['player'].stats.max_mp, libtcod.blue, libtcod.darker_blue)

    # ITEM THINGS

    # Display Items
    if game['item_display_sort'] == 0:
        # value
        to_display_items.sort(key=lambda x: x.s_value, reverse = True)
    elif game['item_display_sort'] == 1:
        # a-z
        to_display_items.sort(key=lambda x: x.q_name)
    elif game['item_display_sort'] == 2:
        # dist
        to_display_items.sort(key=lambda x: x.dist_to_entity(game['player']))
    item_block_start = 17
    item_block_size = 18
    info_panel_console.print_frame(1, item_block_start-1, info_panel_width-2, item_block_size+2, "Nearby Things")
    # fix item buffer in game[]
    if len(to_display_items) == 0:
        MAX_PAGES = 0
    else:
        MAX_PAGES = math.floor((len(to_display_items)-1)/item_block_size)

    if game['item_display_page'] > MAX_PAGES:
        game['item_display_page'] = 0
    if game['item_display_page'] < 0:
        game['item_display_page'] = MAX_PAGES
    
    to_overlay = []
    
    #info_panel_console.print(4, item_block_start + item_block_size, ",./",libtcod.black, libtcod.lighter_gray, libtcod.BKGND_SET, libtcod.LEFT)

    sort = ['$', 'A-Z', 'Dist'][game['item_display_sort']]
    info_panel_console.print(4, item_block_start + item_block_size, "Sort: " + str(sort), 
            libtcod.black, libtcod.lighter_gray, libtcod.BKGND_SET, libtcod.LEFT)

    if MAX_PAGES > 0:
        info_panel_console.print(info_panel_width-4, item_block_start+item_block_size, "PAGE {}/{}".format(game['item_display_page']+1, MAX_PAGES+1),
            libtcod.black, libtcod.lighter_gray, libtcod.BKGND_SET, libtcod.RIGHT)
    if len(to_display_items) >= 0:
        page = game['item_display_page']
        for i, v in enumerate(to_display_items):
            if i >= page*(item_block_size) and i < (page + 1)*(item_block_size):
                info_panel_console.print(5, item_block_start + (i % item_block_size), str(int(v.dist_to_entity(game['player']))), libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                info_panel_console.print(8, item_block_start + (i % item_block_size), v.q_name, libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                info_panel_console.print(info_panel_width-4, item_block_start + (i % item_block_size), str(v.value), libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.RIGHT)
                to_overlay.append(v)
                



    # Display Entities
    if game['entity_display_sort'] == 0:
        to_display_entities.sort(key = lambda x: x.diff, reverse= True)
    elif game['entity_display_sort'] == 1:
        to_display_entities.sort(key = lambda x: x.name)
    elif game['entity_display_sort'] == 2:
        to_display_entities.sort(key = lambda x: x.distance_to(game['player']))

    ent_to_overlay = []
    sort = ['Diff', 'A-Z', 'Dist'][game['entity_display_sort']]

    entity_block_start = item_block_start + item_block_size + 2
    entity_block_size = 21 # ODD!
    info_panel_console.print_frame(1, entity_block_start-1, info_panel_width-2, entity_block_size+2, "Nearby Entities")
    
    if len(to_display_entities) == 0:
        MAX_PAGES = 0
    else:
        MAX_PAGES = math.floor(2*(len(to_display_entities)-1)/(entity_block_size))
    if game['entity_display_page'] > MAX_PAGES:
        game['entity_display_page'] = 0
    if game['entity_display_page'] < 0:
        game['entity_display_page'] = MAX_PAGES

    info_panel_console.print(4, entity_block_start + entity_block_size, "Sort: " + str(sort), 
            libtcod.black, libtcod.lighter_gray, libtcod.BKGND_SET, libtcod.LEFT)

    if MAX_PAGES > 0:
        info_panel_console.print(info_panel_width-4, entity_block_start+entity_block_size, "PAGE {}/{}".format(game['entity_display_page']+1, MAX_PAGES+1),
            libtcod.black, libtcod.lighter_gray, libtcod.BKGND_SET, libtcod.RIGHT)
    count = 0
    if len(to_display_entities) >= 0:
        page = game['entity_display_page']
        for i, v in enumerate(to_display_entities):
            if i*2 >= page*(entity_block_size-1) and i*2 < (page + 1)*(entity_block_size-1):
                count += 1
                info_panel_console.print(5, entity_block_start + 2*(i % int(entity_block_size/2)), str(int(v.distance_to(game['player']))), libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                info_panel_console.print(8, entity_block_start + 2*(i % int(entity_block_size/2)), v.name, libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                info_panel_console.print(info_panel_width-4, entity_block_start + 2*(i % int(entity_block_size/2)), str(v.diff), libtcod.lighter_gray, libtcod.black, libtcod.BKGND_SET, libtcod.RIGHT)
                render_bar(info_panel_console, 2, 1+entity_block_start + 2*(i % int(entity_block_size/2)), int(info_panel_width/2)-2, 
                    v.stats.curr_hp, v.stats.max_hp, libtcod.dark_red, libtcod.darkest_red)
                render_bar(info_panel_console, int(info_panel_width/2), 1+entity_block_start + 2*(i % int(entity_block_size/2)), int(info_panel_width/2)-2, 
                    v.stats.curr_mp, v.stats.max_mp, libtcod.dark_blue, libtcod.darkest_blue)
                ent_to_overlay.append(v)
    info_panel_console.print(2, entity_block_start+entity_block_size-1, ' '*(info_panel_width-4), libtcod.lighter_gray, libtcod.dark_gray, libtcod.BKGND_SET, libtcod.LEFT)
    info_panel_console.print(5, entity_block_start+entity_block_size-1, "0", libtcod.lighter_gray, libtcod.dark_gray, libtcod.BKGND_SET, libtcod.RIGHT)
    info_panel_console.print(8, entity_block_start+entity_block_size-1, game['player'].name, libtcod.lighter_gray, libtcod.dark_gray, libtcod.BKGND_SET, libtcod.LEFT)
    info_panel_console.print(info_panel_width-4, entity_block_start+entity_block_size-1, str(game['player'].diff), libtcod.lighter_gray, libtcod.dark_gray, libtcod.BKGND_SET, libtcod.RIGHT)
    



    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(info_panel_console),
        dest = (
            map_console.width*game['tileset_map'].tile_width,
            game['tileset_text'].tile_height,
            (info_panel_width)*game['tileset_text'].tile_width,
            (info_panel_height)*game['tileset_text'].tile_height
    ))
    

    item_display_renderer = libtcod.Console(1, item_block_size)
    for i, v in enumerate(to_overlay):
        item_display_renderer.print(0, i, v.char, v.color)
    
    game['sdl_renderer'].copy(
        game['console_renderer_map'].render(item_display_renderer),
        dest = (
            map_console.width*game['tileset_map'].tile_width + 2*game['tileset_text'].tile_width,
            game['tileset_text'].tile_height + game['tileset_text'].tile_height*item_block_start,
            game['tileset_text'].tile_height,
            game['tileset_text'].tile_height*item_block_size
    ))


    entity_display_renderer = libtcod.Console(1, int(entity_block_size/2))
    for i, v in enumerate(ent_to_overlay):
        entity_display_renderer.print(0, i, v.char, v.color)
    
    #entity_display_renderer.print(0, entity_block_size-1, str(game['player'].char), game['player'].color)

    game['sdl_renderer'].copy(
        game['console_renderer_map'].render(entity_display_renderer),
        dest = (
            map_console.width*game['tileset_map'].tile_width + 2*game['tileset_text'].tile_width-4,
            game['tileset_text'].tile_height + game['tileset_text'].tile_height*(item_block_size+item_block_start+2),
            game['tileset_text'].tile_height*2,
            game['tileset_text'].tile_height*int(entity_block_size/2)*2
    ))

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
            return(True)
            # libtcod.console_set_default_foreground(con, entity.color)
            # libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)
    return(False)
def draw_item(item, fov_map, game, map_console):
    if libtcod.map_is_in_fov(fov_map, item.x, item.y):
        (x, y) = to_camera_coordinates(item.x, item.y, game)
        if x is not None:
            #set the color and then draw the character that represents this object at its position
            map_console.print(x, y, str(item.char), item.color)
            return(True)
            #libtcod.console_set_default_foreground(con, item.color)
            #libtcod.console_put_char(con, x, y, item.char, libtcod.BKGND_NONE)
    return(False)

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
