import tcod as libtcod

from helper_funcs import gear_lookup

def menu_strip(con, game):
    window = libtcod.console_new(game['screen_width'], 1)
    for i, v in enumerate(['    Ground [g]    ', '  Equipment [e]   ', '  Inventory [i]   ', '     Map [m]      ']):
        if game['option'] == i:
            libtcod.console_set_default_foreground(window, libtcod.white)
            libtcod.console_set_default_background(window, libtcod.gray)
            libtcod.console_print_ex(window, i*18, 0, libtcod.BKGND_ADD, libtcod.LEFT, v)
        else:
            libtcod.console_set_default_foreground(window, libtcod.gray)
            libtcod.console_set_default_background(window, libtcod.black)
            libtcod.console_print_ex(window, i*18, 0, libtcod.BKGND_DEFAULT, libtcod.LEFT, v)
    
    libtcod.console_blit(window, 0, 0, game['screen_width'], 1, 0, 0, 0, 1.0, 0.7)

def equipment_menu(con, game):
    NO_EQUIP = "<empty>"
    slot_height = 2 + len(game['slot_names'])
    slot_width = 10
    for name in game['slot_names']:
        gname = NO_EQUIP
        if game['player'].inventory.wearing[name] is not None:
            gname = game['player'].inventory.wearing[name].name
        
        slot_width = max(slot_width, 5+len(name+gname)+len(name+gname))
    slot_width = 45
    slot_window = libtcod.console_new(slot_width, slot_height)
    libtcod.console_print_frame(slot_window, 0, 0, slot_width, slot_height, True, fmt="Equipped Gear")
    for i, v in enumerate(game['slot_names']):
        l_padding = 10-len(v)
        if game['cursor_0'] == i:
            if game['cursor_spot'] == 0:
                libtcod.console_set_default_foreground(slot_window, libtcod.black)
                libtcod.console_set_default_background(slot_window, libtcod.lighter_yellow)
            else:
                libtcod.console_set_default_foreground(slot_window, libtcod.black)
                libtcod.console_set_default_background(slot_window, libtcod.lighter_gray)
        else:
            libtcod.console_set_default_foreground(slot_window, libtcod.dark_gray)
            libtcod.console_set_default_background(slot_window, libtcod.black)
        libtcod.console_print_ex(slot_window, 12, i+1, libtcod.BKGND_SET, libtcod.RIGHT, " "*l_padding + v+ ": ")

        if game['player'].inventory.wearing[v]:
            r_padding = slot_width-14-len(game['player'].inventory.wearing[v].name)
            if game['cursor_0'] == i:
                libtcod.console_set_default_foreground(slot_window, libtcod.black)
            else:    
                libtcod.console_set_default_foreground(slot_window, libtcod.lighter_gray)
            libtcod.console_print_ex(slot_window, 13, i+1, libtcod.BKGND_SET, libtcod.LEFT, game['player'].inventory.wearing[v].name+r_padding*" ")
        else:
            r_padding = slot_width-14-len(NO_EQUIP)
            if game['cursor_0'] == i:
                libtcod.console_set_default_foreground(slot_window, libtcod.dark_gray)
            else:    
                libtcod.console_set_default_foreground(slot_window, libtcod.darker_gray)
            libtcod.console_print_ex(slot_window, 13, i+1, libtcod.BKGND_SET, libtcod.LEFT, NO_EQUIP+r_padding*" ")


    libtcod.console_blit(slot_window, 0, -1, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    # BAG
    using_bag = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]
    bag_height = max(len(using_bag)+2, 3)
    if using_bag == []:
        bag_width = len(NO_EQUIP) + 3
    else:
        bag_width = max([len(x.q_name) for x in using_bag]) + 5
    bag_window = libtcod.console_new(bag_width, bag_height)
    libtcod.console_print_frame(bag_window, 0, 0, bag_width, bag_height, True, fmt=gear_lookup(game['slot_names'][game['cursor_0']]))

    if len(using_bag) == 0:
        libtcod.console_set_default_foreground(bag_window, libtcod.dark_gray)
        libtcod.console_set_default_background(bag_window, libtcod.black)
        libtcod.console_print_ex(bag_window, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, NO_EQUIP)
    else:
        for i, v in enumerate(using_bag):
            r_padding = max(0, bag_width - len(v.q_name) - 2)
            if game['cursor_1'] == i:
                if game['cursor_spot'] == 1:
                    libtcod.console_set_default_foreground(bag_window, libtcod.black)
                    libtcod.console_set_default_background(bag_window, libtcod.lighter_yellow)
                else:
                    libtcod.console_set_default_foreground(bag_window, libtcod.black)
                    libtcod.console_set_default_background(bag_window, libtcod.lighter_gray)
            else:
                libtcod.console_set_default_foreground(bag_window, libtcod.gray)
                libtcod.console_set_default_background(bag_window, libtcod.black)
            libtcod.console_print_ex(bag_window, 1, i+1, libtcod.BKGND_SET, libtcod.LEFT, v.q_name+r_padding*" ")
            

    libtcod.console_blit(bag_window, 0, -15, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    pass

def ground_menu(con, game, items):
    height = len(items) + 5
    width = 20
    for item in items:
        width = max(width, 9+len(item.name)+len(item.type))
    window = libtcod.console_new(width, height)
    libtcod.console_print_frame(window, 0, 0, width, height, True, fmt="Ground")
    #libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Ground Items")
    if len(items) == 0:
        libtcod.console_set_default_foreground(window, libtcod.dark_gray)
        libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "nothing here...")
    else:

        for i, v in enumerate(items):
            text = ""
            if game['cursor'] == i:
                libtcod.console_set_default_foreground(window, libtcod.white)
                text += "> "
            else:
                libtcod.console_set_default_foreground(window, libtcod.gray)
            text += v.name
            text += " (" + v.type + ")"
            libtcod.console_print_ex(window, 1, i+2, libtcod.BKGND_NONE, libtcod.LEFT, text)


    libtcod.console_blit(window, 0, -1, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

def char_select_menu(con, game):
    window = libtcod.console_new(game['screen_width'], game['screen_height'])
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_set_default_background(window, libtcod.blue)
    libtcod.console_print_rect_ex(window, 0, 0, game['screen_width'], game['screen_height'], libtcod.BKGND_SET, libtcod.LEFT, '')
    libtcod.console_print_ex(window, int(game['screen_width']/2), 1, libtcod.BKGND_NONE, libtcod.CENTER, "Character Select")

    counter = 0
    for race_name in game['options'].keys():
        text = race_name
        if counter == game['cursor_0']:
            text = "> " + text
            if game['cursor_spot'] == 0:
                libtcod.console_set_default_foreground(window, libtcod.yellow)
            else:
                libtcod.console_set_default_foreground(window, libtcod.white)
        else:
            if game['cursor_spot'] == 0:
                libtcod.console_set_default_foreground(window, libtcod.white)
            else:
                libtcod.console_set_default_foreground(window, libtcod.gray)
        libtcod.console_print_ex(window, 10, 20+counter, libtcod.BKGND_NONE, libtcod.LEFT, text)
        counter += 1

    counter = 0
    for selected_class in game['options'][list(game['options'].keys())[game['cursor_0']]]:
        text = selected_class
        if counter == game['cursor_1']:
            text = "> " + text
            if game['cursor_spot'] == 1:
                libtcod.console_set_default_foreground(window, libtcod.yellow)
            else:
                libtcod.console_set_default_foreground(window, libtcod.white)
        else:
            if game['cursor_spot'] == 1:
                libtcod.console_set_default_foreground(window, libtcod.white)
            else:
                libtcod.console_set_default_foreground(window, libtcod.gray)
        libtcod.console_print_ex(window, 25, 20+counter, libtcod.BKGND_NONE, libtcod.LEFT, text)
        counter += 1
    libtcod.console_blit(window, 0, 0, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)


def main_menu(con, background_image, game):
    #libtcod.image_blit_2x(background_image, 0, 0, 0)

    #libtcod.console_set_default_foreground(con, libtcod.white)
    #libtcod.console_put_char(con, 10, 10, 'A', libtcod.BKGND_NONE)

    #libtcod.console_print_ex(con, int(game['screen_width'] / 2), int(game['screen_height'] / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
    #                          'Dragons are Dungeons 3')
    # libtcod.console_print_ex(con, int(game['screen_width'] / 2), int(game['screen_height'] - 2), libtcod.BKGND_NONE, libtcod.CENTER,
    #                          'Teggom')
    width = game['screen_width']
    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, game['screen_height'], '')

    # This is modified
    #height = len(game['options']) + header_height + 10
    height = game['screen_height']
    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_set_default_background(window, libtcod.blue)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_SET, libtcod.LEFT, '')

    # for y in range(50):
    #     libtcod.console_print_ex(window, 0-25, y-25, libtcod.BKGND_NONE, libtcod.LEFT, "abcdefghijklmnopqrstuvwxyz"+str(y)+"zyxwvutsrqponmlkjihgfedcba")
    
    # print all the options
    y = 20 #header_height + 4
    counter = 0
    #libtcod.console_print_ex(window, counter, y+2, libtcod.BKGND_NONE, libtcod.LEFT, "Teggomsssssssssssssssssssssssssss")
    for option_text in game['options']:
        text = option_text
        if counter == game['cursor']:
            text = "> " + text 
        libtcod.console_print_ex(window, counter+10, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        counter += 1
    libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dragons are Dungeons 3')
    libtcod.console_print_ex(window, 2, game['screen_height']-2, libtcod.BKGND_NONE, libtcod.LEFT,
                             'By Teggom')
    
    # blit the contents of "window" to the root console
    x = 0 # int(game['screen_width'] / 2 - width / 2)-15
    y = 0 # int(game['screen_height'] / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    #libtcod.console_blit()
    #menu(con, '', game['options'], 24, game['screen_width'], game['screen_height'], game['cursor'])
# def menu(con, header, options, width, screen_width, screen_height, cursor):
    
    # # calculate total height for the header (after auto-wrap) and one line per option
    # header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)

    # # This is modified
    # height = len(options) + header_height + 10
    # # create an off-screen console that represents the menu's window
    # window = libtcod.console_new(width, height)
    # # print the header, with auto-wrap
    # libtcod.console_set_default_foreground(window, libtcod.white)
    # libtcod.console_set_default_background(window, libtcod.blue)
    # libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_SET, libtcod.LEFT, header)

    # # for y in range(50):
    # #     libtcod.console_print_ex(window, 0-25, y-25, libtcod.BKGND_NONE, libtcod.LEFT, "abcdefghijklmnopqrstuvwxyz"+str(y)+"zyxwvutsrqponmlkjihgfedcba")
    
    # # print all the options
    # y = header_height + 4
    # counter = 0
    # #libtcod.console_print_ex(window, counter, y+2, libtcod.BKGND_NONE, libtcod.LEFT, "Teggomsssssssssssssssssssssssssss")
    # for option_text in options:
    #     text = option_text
    #     if counter == cursor:
    #         text = "> " + text 
    #     libtcod.console_print_ex(window, counter, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
    #     y += 1
    #     counter += 1
    # libtcod.console_print_ex(window, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT,
    #                          'Dragons are Dungeons 3')
    # libtcod.console_print_ex(window, counter, y+4, libtcod.BKGND_NONE, libtcod.CENTER,
    #                          'By Teggom')
    
    # # blit the contents of "window" to the root console
    # x = int(screen_width / 2 - width / 2)-15
    # y = int(screen_height / 2 - height / 2)
    # libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    # #libtcod.console_blit()
