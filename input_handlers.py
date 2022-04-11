import libtcodpy as libtcod

def handle_charselect_keys(key):
    if key.vk == libtcod.KEY_UP:
        return({'move' : -1})
    if key.vk == libtcod.KEY_DOWN:
        return({'move' : 1})
    if key.vk == libtcod.KEY_RIGHT:
        return({'select' : True})
    if key.vk == libtcod.KEY_LEFT:
        return({'back' : True})
    if key.vk == libtcod.KEY_ENTER:
        return({'select' : True})
    if key.vk == libtcod.KEY_ESCAPE:
        return({'exit' : True})
    return({})


def handle_mainmenu_keys(key):
    if key.vk == libtcod.KEY_UP:
        return({'move' : -1})
    if key.vk == libtcod.KEY_DOWN:
        return({'move' : 1})
    if key.vk == libtcod.KEY_ENTER:
        return({'select' : True})
    if key.vk == libtcod.KEY_ESCAPE:
        return({'exit' : True})
    return({})

def handle_playerturn_keys(key):
    # Movement keys
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}