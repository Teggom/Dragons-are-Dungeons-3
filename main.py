import libtcodpy as libtcod
from time import sleep
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, render_animations
from game_states import GameStates
from animations import animation
from unit_stats.ai import BasicMerchant, Wander

def main():
    screen_width = 80
    screen_height = 50

    # Size of the map
    map_width = 80
    map_height = 45

    # Some variables for the rooms in the map
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 4
    fov_light_walls = True

    game_state = GameStates.PLAYER_TURN

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white, "Player", "Goblin")
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.red, "Human Merchant", "Human", blocks = True, ai=BasicMerchant())
    npc2 = Entity(int(screen_width / 2 + 5), int(screen_height / 2 + 5), '@', libtcod.green, "Lost Elf", "Elf", blocks = True, ai=Wander())
    entities = [player, npc, npc2]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, 1, 1)
    animations = []
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, player.stats.fov, fov_light_walls, fov_algorithm)

        render_all(con, player, entities, game_map, fov_map, fov_recompute, screen_width, screen_height)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)
                    fov_recompute = True
            game_state = GameStates.ENEMY_TURN

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player, fov_map, game_map, entities)
            game_state = GameStates.PLAYER_TURN



        # if game_state == GameStates.GRAPHICAL:
        #     print("Graphics")
        #     to_rend = []
        #     game_state = GameStates.PLAYER_TURN
        #     for ani in animations:
        #         if not ani.finished:
        #             to_rend.append(ani)
        #             print("\t Ani found")
        #     while len(to_rend) > 0:
        #         sleep(1/4)
        #         recompute_fov(fov_map, player.x, player.y, player.stats.fov, fov_light_walls, fov_algorithm)
        #         render_all(con, player, entities, game_map, fov_map, fov_recompute, screen_width, screen_height)
        #         render_animations(con, to_rend, fov_map)
        #         libtcod.console_flush()
        #         clear_all(con, entities)
        #         to_rend = []
        #         for ani in animations:
        #             if not ani.finished:
        #                 to_rend.append(ani)
        #         print(len(to_rend))

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
     main()