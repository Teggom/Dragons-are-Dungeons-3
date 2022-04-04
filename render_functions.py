import libtcodpy as libtcod


def render_all(con, player, entities, game_map, fov_map, fov_recompute, screen_width, screen_height):
    if fov_recompute:
    # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[x][y].get_color("Visible"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[x][y].get_color("Visible"), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                    game_map.tiles[x][y].last_seen = 0

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[x][y].get_color("Explored"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[x][y].get_color("Explored"), libtcod.BKGND_SET)

                
                if game_map.tiles[x][y].explored and not visible:
                    if game_map.tiles[x][y].step(player):
                        libtcod.console_set_char_background(con, x, y, game_map.tiles[x][y].get_color("Unseen"), libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)