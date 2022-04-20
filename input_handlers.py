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

def handle_ground_menu_keys(key):
    if key.vk == libtcod.KEY_UP:
        return({'move' : -1})
    if key.vk == libtcod.KEY_DOWN:
        return({'move' : 1})
    if key.vk == libtcod.KEY_ENTER:
        return({'select' : True})
    if key.vk == libtcod.KEY_ESCAPE:
        return({'exit' : True})
    if key.text == 'g':
        return({'exit' : True})
    if key.vk == libtcod.KEY_PAGEDOWN:
        return({'jump' : "down"})
    if key.vk == libtcod.KEY_PAGEUP:
        return({'jump' : "up"})

    return({})

def handle_equipment_menu_keys(key):
    if key.vk == libtcod.KEY_UP:
        return({'move' : -1})
    if key.vk == libtcod.KEY_DOWN:
        return({'move' : 1})
    if key.vk == libtcod.KEY_ENTER:
        return({'select' : True})
    if key.vk == libtcod.KEY_RIGHT:
        return({'select' : True})
    if key.vk == libtcod.KEY_LEFT:
        return({"back" : True})
    if key.vk == libtcod.KEY_ESCAPE:
        return({'exit' : True})
    if key.text == 'e':
        return({'exit' : True})
    if key.text == 'd':
        return({'drop' : True})
    if key.vk == libtcod.KEY_PAGEDOWN:
        return({'jump' : "down"})
    if key.vk == libtcod.KEY_PAGEUP:
        return({'jump' : "up"})
    if key.vk == libtcod.KEY_TAB:
        return({'tab' : True})
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
    elif key.text == 'g':
        return {'ground_menu_opened' : True}
    elif key.text == 'e':
        return {'equipment_menu_opened' : True}
    elif key.text == 'i':
        return {'inventory_menu_opened' : True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}