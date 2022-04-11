import tcod as libtcod

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
