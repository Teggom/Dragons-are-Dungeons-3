import enum
import math
import time
import tcod as libtcod
from textwrap import wrap
from helper_funcs import gear_lookup

def menu_strip(game):
    strip_console = libtcod.Console(int(game['screen_width']*game['tileset_map'].tile_width/game['tileset_text'].tile_width), 1)
    #window = libtcod.console_new(game['screen_width'], 1)
    elements = [
        [["G", 'round'], 0],
        [['Eq', 'u', 'ipment'], 1],
        [['B', 'ags'], 0],
        [['L', 'ook'], 0],
        [['I', 'nteract'], 0],
        [['P', 'erform'], 0]
    ]
    for i, v in enumerate(elements):
        text = ""
        for elem in v[0]:
            text += elem
        if game['option'] == i:
            strip_console.print(i*18-5, 0, " "*18, libtcod.white, libtcod.gray, libtcod.BKGND_SET, libtcod.LEFT)
            strip_console.print(i*18, 0, text, libtcod.black, libtcod.gray, libtcod.BKGND_NONE, libtcod.LEFT)
        else:
            dist = 0
            for j, k in enumerate(v[0]):
                if j == v[1]:
                    strip_console.print(i*18+dist, 0, k, libtcod.darker_yellow, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                else:
                    strip_console.print(i*18+dist, 0, k, libtcod.gray, libtcod.black, libtcod.BKGND_SET, libtcod.LEFT)
                dist += len(k)
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(strip_console),
        dest = (
            0,
            0,
            strip_console.width*game['tileset_text'].tile_width,
            strip_console.height*game['tileset_text'].tile_height
        )
    )
    

def equipment_menu(game):
    NO_EQUIP = "<empty>"
    slot_height = 2 + len(game['slot_names'])
    slot_width = 10
    for name in game['slot_names']:
        gname = NO_EQUIP
        if game['player'].inventory.wearing[name] is not None:
            gname = game['player'].inventory.wearing[name].t_name
        
        slot_width = max(slot_width, 5+len(name+gname)+len(name+gname))
    slot_width = 45
    slot_console = libtcod.Console(slot_width, slot_height)
    slot_console.draw_frame(0, 0, slot_width, slot_height, "Equipped Gear")
    for i, v in enumerate(game['slot_names']):
        l_padding = 10-len(v)
        if game['cursor_0'] == i:
            if game['cursor_spot'] == 0:
                slot_console.print(12, i+1, " "*l_padding + v+ ": ", libtcod.black, libtcod.lighter_yellow, alignment=libtcod.RIGHT)
            else:
                slot_console.print(12, i+1, " "*l_padding + v+ ": ", libtcod.black, libtcod.lighter_gray, alignment=libtcod.RIGHT)
        else:
            slot_console.print(12, i+1, " "*l_padding + v+ ": ", libtcod.dark_gray, libtcod.black, alignment=libtcod.RIGHT)

        if game['player'].inventory.wearing[v]:
            r_padding = slot_width-14-len(game['player'].inventory.wearing[v].t_name)
            if game['cursor_0'] == i:
                if game['cursor_spot'] == 0:
                    slot_console.print(13, i+1, game['player'].inventory.wearing[v].t_name+r_padding*" ", libtcod.black, libtcod.lighter_yellow)
                else:
                    slot_console.print(13, i+1, game['player'].inventory.wearing[v].t_name+r_padding*" ", libtcod.black, libtcod.lighter_gray)
            else:    
                slot_console.print(13, i+1, game['player'].inventory.wearing[v].t_name+r_padding*" ", libtcod.lighter_gray)
        else:
            r_padding = slot_width-14-len(NO_EQUIP)
            if game['cursor_0'] == i:
                if game['cursor_spot'] == 0:
                    slot_console.print(13, i+1, NO_EQUIP+r_padding*" ", libtcod.black, libtcod.lighter_yellow)
                else:
                    slot_console.print(13, i+1, NO_EQUIP+r_padding*" ", libtcod.black, libtcod.lighter_gray)
            else:    
                slot_console.print(13, i+1, NO_EQUIP+r_padding*" ", libtcod.darker_gray)
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(slot_console),
        dest = (
            10,
            16,
            slot_console.width*game['tileset_text'].tile_width,
            slot_console.height*game['tileset_text'].tile_height
        )
    )

    # BAG
    using_bag = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]
    bag_height = len(game['slot_names'])+2
    bag_width = 34
    bag_console = libtcod.Console(bag_width, bag_height)
    bag_console.print_frame(0, 0, bag_width, bag_height, gear_lookup(game['slot_names'][game['cursor_0']]))

    if len(using_bag) == 0:
        bag_console.print(1, 1, NO_EQUIP, libtcod.dark_gray, libtcod.black)
    else:
        page = int(game['cursor_1']/(bag_height-2))
        for i, v in enumerate(using_bag):
            if i >= page*(bag_height-2) and i < (page+1)*(bag_height-2):                    
                r_padding = max(0, bag_width - len(v.q_name) - 2)
                if game['cursor_1'] == i:
                    if game['cursor_spot'] == 1:
                        bag_console.print(1, i+1-page*(bag_height-2), v.q_name+r_padding*" ", libtcod.black, libtcod.lighter_yellow)
                    else:
                        bag_console.print(1, i+1-page*(bag_height-2), v.q_name+r_padding*" ", libtcod.black, libtcod.lighter_gray)
                else:
                    bag_console.print(1, i+1-page*(bag_height-2), v.q_name+r_padding*" ", libtcod.gray, libtcod.black)
                
        bag_console.print(bag_width-2, bag_height-1, "page {}/{}".format(page+1, int(1+len(using_bag)/bag_height)), libtcod.black, libtcod.lighter_gray, alignment=libtcod.RIGHT)
        

    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(bag_console),
        dest = (
            10+slot_console.width*game['tileset_text'].tile_width+10,
            16,
            bag_console.width*game['tileset_text'].tile_width,
            bag_console.height*game['tileset_text'].tile_height
        )
    )
    
    
    draw_character_stat_menu(chara_height=43, chara_width=80, pos_x= 10, pos_y=bag_console.height*game['tileset_text'].tile_height+16*2, game=game)
    
    imenu_x_start = 10 + 10+slot_console.width*game['tileset_text'].tile_width+10 + bag_console.width*game['tileset_text'].tile_width
    ret_size, ret_groups = draw_item_stat_menu(item_height = 45, item_width = 42, x_pos = -bag_width-slot_width-3, y_pos = -2, game=game, draw = False)
    if ret_size > 3:
        draw_item_stat_menu(item_height = ret_size-2+len(ret_groups), item_width = 42, x_pos = imenu_x_start, y_pos=game['tileset_text'].tile_height, game=game, draw=True, to_draw = ret_groups)
    pass
    game['sdl_renderer'].present()

def draw_item_stat_menu(item_height, item_width, x_pos, y_pos, game, draw = True, to_draw = ['stats', 'skills', 'resistances']):
    item_console = libtcod.Console(item_width, item_height)
    item_console.print_frame(0, 0, item_width, item_height, "Item")
    text_indent = 15
    old_value_indent = 21
    arrow_indent = 26
    new_value_indent = 31
    
    s_drop = 3
    stat_drop = s_drop+4
    skill_drop = stat_drop+10
    resistance_drop = skill_drop + 12
    
    

    base_color = libtcod.lighter_gray
    decrease_color = libtcod.red
    same_color = libtcod.darker_gray
    increase_color = libtcod.green

    header_fore = libtcod.black
    header_back = libtcod.gray

    draw_line_drop = s_drop
    using_bag = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]
    
    (fg, bg) = libtcod.black, libtcod.lighter_gray
    
    for i in range(item_height-3):
        if i % 2 == 0:
            bg = libtcod.black
        else:
            bg = libtcod.darkest_gray
        item_console.print(1, i+2, " "*(item_width-2), fg, bg, libtcod.BKGND_ADD)

    (fg, bg) = (libtcod.lighter_gray, libtcod.black)

    if game['cursor_spot'] == 0:
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
        else:
            item = None
    else:
        item = using_bag[game['cursor_1']]
    
    draw_stats = False
    draw_skills = False
    draw_resistances = False

    if item:
        name = wrap(item.name, item_width-2)
        item_console.print(int(item_width/2), 1, name[0], fg, bg, libtcod.BKGND_NONE, libtcod.CENTER)
        if len(name) == 2:
            item_console.print(int(item_width/2), 2, name[1], fg, bg, libtcod.BKGND_NONE, libtcod.CENTER)
        
        item_console.print(text_indent, draw_line_drop, "Rarity:", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
        item_console.print(old_value_indent, draw_line_drop, "TODO", fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
        draw_line_drop += 1
        
        item_console.print(text_indent, draw_line_drop, "Value:", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
        item_console.print(old_value_indent, draw_line_drop, "TODO", fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
        draw_line_drop += 1

        item_console.print(text_indent, draw_line_drop, "Type:", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
        item_console.print(old_value_indent, draw_line_drop, item.type, fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
        draw_line_drop += 1

        fg = libtcod.lighter_yellow

        if item.type == 'Weapon':
            (fg, bg) = (header_fore, header_back)
            item_console.print(old_value_indent, draw_line_drop, "DAMAGE", fg, bg, libtcod.BKGND_SET, libtcod.CENTER)
            draw_line_drop += 1
            fg = base_color
            avg = 0
            for dmg in item.damages:
                avg += int(dmg.avg)
                # TODO change first print's colors based on damage type?
                item_console.print(text_indent, draw_line_drop, dmg.name, fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                item_console.print(old_value_indent, draw_line_drop, "Average: {}".format(int(dmg.avg)), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                item_console.print(new_value_indent+2, draw_line_drop, "("+dmg.type+")", fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                draw_line_drop += 1
            if item.trait and len(item.trait.on_item['onhit_damage']) > 0:
                for dmg in item.trait.on_item['onhit_damage']:
                    avg += int(dmg.avg)
                    # TODO change first print's colors based on damage type?
                    item_console.print(text_indent, draw_line_drop, dmg.name, fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                    item_console.print(old_value_indent, draw_line_drop, "Average: {}".format(int(dmg.avg)), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                    item_console.print(new_value_indent+2, draw_line_drop, "("+dmg.type+")", fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                    draw_line_drop += 1

            item_console.print(arrow_indent, draw_line_drop, "Total Average: {}".format(avg), fg, bg, libtcod.BKGND_NONE, libtcod.CENTER)
            draw_line_drop += 1  



        # MAKE
        # in green
        # Strength: 20 -> 23   (+3)
        # in red
        #   Wisdom: 20 -> 0    (-20)
        # in gray
        # Charisma: 13 -> 13   (0)
        

        if "stats" in to_draw:
            (fg, bg) = (header_fore, header_back)
            item_console.print(old_value_indent, draw_line_drop, "STATS", fg, bg, libtcod.BKGND_SET, libtcod.CENTER)
            draw_line_drop += 1
            stat_raw_names = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'luck', 'memory', 'sight', 'perception']
            stat_pt_names = ["Strength", "Dexterity", "Intelligence", "Wisdom", "Charisma", "Luck", "Memory", "Sight", "Perception"]
            for i in range(len(stat_raw_names)):
                cur_stat = stat_raw_names[i]
                new_stat = 0
                if item.stats.get(cur_stat):
                    new_stat += item.stats.get(cur_stat)
                if item.trait:
                    if item.trait.on_item['stats'].get(cur_stat): # FOR ALL INSTANCES, CHANGE item.trait.on_item['stats'].get(cur_stat) -> item.trait.on_item['stats'].get(cur_stat)
                        new_stat += item.trait.on_item['stats'].get(cur_stat) #TODO FIND AND REPLCE on_item['stats'] check for skills, resistances with on_char. check on_char and on_item on other menus too
                for cond in item.conditions:
                    if cond.on_item['stats'].get(cur_stat):
                        new_stat += cond.on_item['stats'].get(cur_stat)
                old_stat = 0
                if game['slot_names'][game['cursor_0']] in ['Left Hand', 'Right Hand']:
                    # Looking at weapon
                    # Check which menu we are in, cursor_spot
                    if game['cursor_spot'] == 0:
                        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.stats.get(cur_stat):
                                old_stat += old_item.stats.get(cur_stat)
                            if old_item.trait:
                                if old_item.trait.on_item['stats'].get(cur_stat):
                                    old_stat += old_item.trait.on_item['stats'].get(cur_stat)
                            for cond in old_item.conditions:
                                if cond.on_item['stats'].get(cur_stat):
                                    old_stat += cond.on_item['stats'].get(cur_stat)
                    else:
                        # in bag looking at replacing items
                        if game['player'].inventory.wearing['Left Hand'] or game['player'].inventory.wearing['Right Hand']:
                            old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                            else:
                                old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                            # # # wearing single hand
                            # equiping same single hand
                            if not item.twohand:
                                if old_item_samehand and old_item_samehand.twohand==False:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['stats'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['stats'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['stats'].get(cur_stat):
                                            old_stat += cond.on_item['stats'].get(cur_stat)
                                elif old_item_offhand or old_item_samehand:
                                    replace_twohand = False
                                    if old_item_offhand:
                                        if old_item_offhand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_offhand
                                    if old_item_samehand:
                                        if old_item_samehand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_samehand
                                    if replace_twohand:
                                        if old_item.stats.get(cur_stat):
                                            old_stat += old_item.stats.get(cur_stat)
                                        if old_item.trait:
                                            if old_item.trait.on_item['stats'].get(cur_stat):
                                                old_stat += old_item.trait.on_item['stats'].get(cur_stat)
                                        for cond in old_item.conditions:
                                            if cond.on_item['stats'].get(cur_stat):
                                                old_stat += cond.on_item['stats'].get(cur_stat)
                            if item.twohand:
                                old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                                if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                    old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                                else:
                                    old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                                if old_item_samehand and old_item_offhand:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['stats'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['stats'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['stats'].get(cur_stat):
                                            old_stat += cond.on_item['stats'].get(cur_stat)
                                    if old_item_offhand.stats.get(cur_stat):
                                        old_stat += old_item_offhand.stats.get(cur_stat)
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['stats'].get(cur_stat):
                                            old_stat += old_item_offhand.trait.on_item['stats'].get(cur_stat)
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['stats'].get(cur_stat):
                                            old_stat += cond.on_item['stats'].get(cur_stat)
                                elif old_item_samehand:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['stats'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['stats'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['stats'].get(cur_stat):
                                            old_stat += cond.on_item['stats'].get(cur_stat)
                                elif old_item_offhand:
                                    if old_item_offhand.stats.get(cur_stat):
                                        old_stat += old_item_offhand.stats.get(cur_stat)
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['stats'].get(cur_stat):
                                            old_stat += old_item_offhand.trait.on_item['stats'].get(cur_stat)
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['stats'].get(cur_stat):
                                            old_stat += cond.on_item['stats'].get(cur_stat)
                else:
                    if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.stats.get(cur_stat):
                                old_stat += old_item.stats.get(cur_stat)
                            if old_item.trait:
                                if old_item.trait.on_item['stats'].get(cur_stat):
                                    old_stat += old_item.trait.on_item['stats'].get(cur_stat)
                            for cond in old_item.conditions:
                                if cond.on_item['stats'].get(cur_stat):
                                    old_stat += cond.on_item['stats'].get(cur_stat)
                
                if game['cursor_spot'] == 0:
                    if new_stat == 0:
                        fg = same_color
                    if new_stat != 0:
                        fg = base_color
                        item_console.print(text_indent, draw_line_drop, stat_pt_names[i] + ":", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(new_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_stats = True
                        draw_line_drop += 1

                else:
                    if new_stat != 0 or old_stat != 0:
                        fg = base_color
                        if new_stat == old_stat:
                            fg = same_color
                        
                        item_console.print(text_indent, draw_line_drop, stat_pt_names[i] + ":", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(arrow_indent, draw_line_drop, "->", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(old_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        if old_stat > new_stat:
                            fg = decrease_color
                        elif old_stat < new_stat:
                            fg = increase_color
                        else:
                            fg = same_color
                        item_console.print(new_value_indent, draw_line_drop, str(new_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_stats = True
                        draw_line_drop += 1

        if 'skills' in to_draw:
            (fg, bg) = (header_fore, header_back)
            item_console.print(old_value_indent, draw_line_drop, "SKILLS", fg, bg, libtcod.BKGND_SET, libtcod.CENTER)
            
            draw_line_drop += 1
            skill_raw_names = ['athletics', 'acrobatics', 'slight_of_hand', 'stealth', 'arcana', 'alchemy', 'crafting', 'bartering', 'persuasion', 'intimidation', 'deception']
            skill_pt_names = ["Athletics", 'Acrobatics', 'Slight of Hand', 'Stealth', 'Arcana', 'Alchemy', 'Crafting', 'Bartering', "Persuasion", 'Intimidation', "Deception"]
            for i in range(len(skill_raw_names)):
                cur_stat = skill_raw_names[i]
                #print(cur_stat, stat_drop)
                new_stat = 0
                if item.skills.get(cur_stat):
                    new_stat += item.skills.get(cur_stat)
                if item.trait:
                    if item.trait.on_item['skills'].get(cur_stat):
                        new_stat += item.trait.on_item['skills'].get(cur_stat)
                for cond in item.conditions:
                    if cond.on_item['skills'].get(cur_stat):
                        new_stat += cond.on_item['skills'].get(cur_stat)
                old_stat = 0
                if game['slot_names'][game['cursor_0']] in ['Left Hand', 'Right Hand']:
                    # Looking at weapon
                    # Check which menu we are in, cursor_spot
                    if game['cursor_spot'] == 0:
                        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.skills.get(cur_stat):
                                old_stat += old_item.skills.get(cur_stat)
                            if old_item.trait:
                                if old_item.trait.on_item['skills'].get(cur_stat):
                                    old_stat += old_item.trait.on_item['skills'].get(cur_stat)
                            for cond in old_item.conditions:
                                if cond.on_item['skills'].get(cur_stat):
                                    old_stat += cond.on_item['skills'].get(cur_stat)
                    else:
                        # in bag looking at replacing items
                        if game['player'].inventory.wearing['Left Hand'] or game['player'].inventory.wearing['Right Hand']:
                            old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                            else:
                                old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                            # # # wearing single hand
                            # equiping same single hand
                            if not item.twohand:
                                if old_item_samehand and old_item_samehand.twohand==False:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['skills'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['skills'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['skills'].get(cur_stat):
                                            old_stat += cond.on_item['skills'].get(cur_stat)
                                elif old_item_offhand or old_item_samehand:
                                    replace_twohand = False
                                    if old_item_offhand:
                                        if old_item_offhand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_offhand
                                    if old_item_samehand:
                                        if old_item_samehand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_samehand
                                    if replace_twohand:
                                        if old_item.stats.get(cur_stat):
                                            old_stat += old_item.stats.get(cur_stat)
                                        if old_item.trait:
                                            if old_item.trait.on_item['skills'].get(cur_stat):
                                                old_stat += old_item.trait.on_item['skills'].get(cur_stat)
                                        for cond in old_item.conditions:
                                            if cond.on_item['skills'].get(cur_stat):
                                                old_stat += cond.on_item['skills'].get(cur_stat)
                            if item.twohand:
                                old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                                if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                    old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                                else:
                                    old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                                if old_item_samehand and old_item_offhand:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['skills'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['skills'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['skills'].get(cur_stat):
                                            old_stat += cond.on_item['skills'].get(cur_stat)
                                    if old_item_offhand.stats.get(cur_stat):
                                        old_stat += old_item_offhand.stats.get(cur_stat)
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['skills'].get(cur_stat):
                                            old_stat += old_item_offhand.trait.on_item['skills'].get(cur_stat)
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['skills'].get(cur_stat):
                                            old_stat += cond.on_item['skills'].get(cur_stat)
                                elif old_item_samehand:
                                    if old_item_samehand.stats.get(cur_stat):
                                        old_stat += old_item_samehand.stats.get(cur_stat)
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['skills'].get(cur_stat):
                                            old_stat += old_item_samehand.trait.on_item['skills'].get(cur_stat)
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['skills'].get(cur_stat):
                                            old_stat += cond.on_item['skills'].get(cur_stat)
                                elif old_item_offhand:
                                    if old_item_offhand.stats.get(cur_stat):
                                        old_stat += old_item_offhand.stats.get(cur_stat)
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['skills'].get(cur_stat):
                                            old_stat += old_item_offhand.trait.on_item['skills'].get(cur_stat)
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['skills'].get(cur_stat):
                                            old_stat += cond.on_item['skills'].get(cur_stat)
                else:
                    if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.stats.get(cur_stat):
                                old_stat += old_item.stats.get(cur_stat)
                            if old_item.trait:
                                if old_item.trait.on_item['skills'].get(cur_stat):
                                    old_stat += old_item.trait.on_item['skills'].get(cur_stat)
                            for cond in old_item.conditions:
                                if cond.on_item['skills'].get(cur_stat):
                                    old_stat += cond.on_item['skills'].get(cur_stat)
                
                if game['cursor_spot'] == 0:
                    if new_stat == 0:
                        fg = same_color
                    if new_stat != 0:
                        fg = base_color
                        item_console.print(text_indent, draw_line_drop, skill_pt_names[i] + ":", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(new_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_line_drop += 1
                        draw_skills = True

                else:
                    if new_stat != 0 or old_stat != 0:
                        fg = base_color
                        if new_stat == old_stat:
                            fg = same_color
                        item_console.print(text_indent, draw_line_drop, skill_pt_names[i] + ":", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(arrow_indent, draw_line_drop, "->", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(old_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        if old_stat > new_stat:
                            fg = decrease_color
                        elif old_stat < new_stat:
                            fg = increase_color
                        else:
                            fg = same_color
                        item_console.print(new_value_indent, draw_line_drop, str(new_stat), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_line_drop += 1
                        draw_skills = True

        if 'resistances' in to_draw:
            (fg, bg) = (header_fore, header_back)
            item_console.print(old_value_indent, draw_line_drop, "RESISTANCES", fg, bg, libtcod.BKGND_SET, libtcod.CENTER)
            
            draw_line_drop += 1
            res_raw_names = ['slash', 'pierce', 'blunt', 'fire', 'frost', 'shock', 'arcane', 'poison', 'holy', 'unholy']
            res_pt_names = ['Slash', 'Pierce', 'Blunt', 'Fire', "Frost", 'Shock', 'Arcane', 'Poison', 'Holy', 'Unholy']
            for i in range(len(res_raw_names)):
                cur_res = res_raw_names[i]
                #print(cur_stat, stat_drop)
                new_res = 0
                if item.resistances.get(cur_res + "_resistance"):
                    new_res += item.resistances.get(cur_res + "_resistance")
                if item.trait:
                    if item.trait.on_item['resistances'].get(cur_res + "_resistance"):
                        new_res += item.trait.on_item['resistances'].get(cur_res + "_resistance")
                for cond in item.conditions:
                    if cond.on_item['resistances'].get(cur_res + "_resistance"):
                        new_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                old_res = 0
                if game['slot_names'][game['cursor_0']] in ['Left Hand', 'Right Hand']:
                    # Looking at weapon
                    # Check which menu we are in, cursor_spot
                    if game['cursor_spot'] == 0:
                        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.resistances.get(cur_res + "_resistance"):
                                old_res += old_item.resistances.get(cur_res + "_resistance")
                            if old_item.trait:
                                if old_item.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                    old_res += old_item.trait.on_item['resistances'].get(cur_res + "_resistance")
                            for cond in old_item.conditions:
                                if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                    old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                    else:
                        # in bag looking at replacing items
                        if game['player'].inventory.wearing['Left Hand'] or game['player'].inventory.wearing['Right Hand']:
                            old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                            else:
                                old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                            # # # wearing single hand
                            # equiping same single hand
                            if not item.twohand:
                                if old_item_samehand and old_item_samehand.twohand==False:
                                    if old_item_samehand.resistances.get(cur_res + "_resistance"):
                                        old_res += old_item_samehand.resistances.get(cur_res + "_resistance")
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance")
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                                elif old_item_offhand or old_item_samehand:
                                    replace_twohand = False
                                    if old_item_offhand:
                                        if old_item_offhand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_offhand
                                    if old_item_samehand:
                                        if old_item_samehand.twohand:
                                            replace_twohand = True
                                            old_item = old_item_samehand
                                    if replace_twohand:
                                        if old_item.resistances.get(cur_res + "_resistance"):
                                            old_res += old_item.resistances.get(cur_res + "_resistance")
                                        if old_item.trait:
                                            if old_item.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                                old_res += old_item.trait.on_item['resistances'].get(cur_res + "_resistance")
                                        for cond in old_item.conditions:
                                            if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                                old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                            if item.twohand:
                                old_item_samehand = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                                if game['slot_names'][game['cursor_0']] == 'Left Hand':
                                    old_item_offhand = game['player'].inventory.wearing["Right Hand"]
                                else:
                                    old_item_offhand = game['player'].inventory.wearing["Left Hand"]
                                if old_item_samehand and old_item_offhand:
                                    if old_item_samehand.resistances.get(cur_res + "_resistance"):
                                        old_res += old_item_samehand.resistances.get(cur_res + "_resistance")
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance")
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                                    if old_item_offhand.resistances.get(cur_res + "_resistance"):
                                        old_res += old_item_offhand.resistances.get(cur_res + "_resistance")
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += old_item_offhand.trait.on_item['resistances'].get(cur_res + "_resistance")
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                                elif old_item_samehand:
                                    if old_item_samehand.resistances.get(cur_res + "_resistance"):
                                        old_res += old_item_samehand.resistances.get(cur_res + "_resistance")
                                    if old_item_samehand.trait:
                                        if old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += old_item_samehand.trait.on_item['resistances'].get(cur_res + "_resistance")
                                    for cond in old_item_samehand.conditions:
                                        if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                                elif old_item_offhand:
                                    if old_item_offhand.resistances.get(cur_res + "_resistance"):
                                        old_res += old_item_offhand.resistances.get(cur_res + "_resistance")
                                    if old_item_offhand.trait:
                                        if old_item_offhand.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += old_item_offhand.trait.on_item['resistances'].get(cur_res + "_resistance")
                                    for cond in old_item_offhand.conditions:
                                        if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                            old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                else:
                    if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
                            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
                            if old_item.resistances.get(cur_res + "_resistance"):
                                old_res += old_item.resistances.get(cur_res + "_resistance")
                            if old_item.trait:
                                if old_item.trait.on_item['resistances'].get(cur_res + "_resistance"):
                                    old_res += old_item.trait.on_item['resistances'].get(cur_res + "_resistance")
                            for cond in old_item.conditions:
                                if cond.on_item['resistances'].get(cur_res + "_resistance"):
                                    old_res += cond.on_item['resistances'].get(cur_res + "_resistance")
                
                if game['cursor_spot'] == 0:
                    if new_res == 0:
                        fg = same_color
                    if new_res != 0:
                        fg = base_color
                        item_console.print(text_indent, draw_line_drop, res_pt_names[i] + " Resist:", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(new_res), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_line_drop += 1
                        draw_resistances = True

                else:
                    if new_res != 0 or old_res != 0:
                        fg = base_color
                        if new_res == old_res:
                            fg = same_color
                        item_console.print(text_indent, draw_line_drop, res_pt_names[i] + " Resist:", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(arrow_indent, draw_line_drop, "->", fg, bg, libtcod.BKGND_NONE, libtcod.RIGHT)
                        item_console.print(old_value_indent, draw_line_drop, str(old_res), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        if old_res > new_res:
                            fg = decrease_color
                        elif old_res < new_res:
                            fg = increase_color
                        else:
                            fg = same_color
                        item_console.print(new_value_indent, draw_line_drop, str(new_res), fg, bg, libtcod.BKGND_NONE, libtcod.LEFT)
                        draw_line_drop += 1
                        draw_resistances = True

    if draw:
        game['sdl_renderer'].copy(
            game['console_renderer_text'].render(item_console),
            dest = (
                x_pos,
                y_pos,
                item_console.width*game['tileset_text'].tile_width,
                item_console.height*game['tileset_text'].tile_height
            )
        )
    else:
        drawing = []
        if draw_stats:
            drawing.append('stats')
        if draw_skills:
            drawing.append('skills')
        if draw_resistances:
            drawing.append('resistances')
        return((draw_line_drop, drawing))


def ground_menu(game, items):
    
    height = 15 #len(items) + 5
    width = 33
    ground_console = libtcod.Console(width, height)
    ground_console.draw_frame(0,0,width,height,"Ground")
    if len(items) == 0:
        ground_console.print(1, 1, "Nothing here...", libtcod.gray)
    else:
        page = int(game['cursor']/(height-2))
        for i, v in enumerate(items):
            if i >= page*(height-2) and i < (page+1)*(height-2):
                text = ""
                if game['cursor'] == i:

                    ground_console.print(1, i+1-page*(height-2), v.q_name, libtcod.black, libtcod.lighter_yellow)
                else:

                    ground_console.print(1, i+1-page*(height-2), v.q_name, libtcod.gray, libtcod.black)
                text += v.name

        ground_console.print(width-2, height-1, "page {}/{}".format(page+1, int(1+len(items)/height)), libtcod.black, libtcod.lighter_gray, alignment=libtcod.RIGHT)
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(ground_console),
        dest = (
            10,
            16,
            ground_console.width*game['tileset_text'].tile_width,
            ground_console.height*game['tileset_text'].tile_height
        )
    )
    game['sdl_renderer'].present()

def char_select_menu(game):
    char_select_console = libtcod.Console(30, 30)
    blank_console = libtcod.Console(1, 1)
    
    counter = 0
    for race_name in game['options'].keys():
        if counter == game['cursor_0']:
            char_select_console.print(0, counter, race_name, libtcod.black, libtcod.yellow, bg_blend = libtcod.BKGND_SET)
        else:
            char_select_console.print(0, counter, race_name, libtcod.white, libtcod.black, bg_blend = libtcod.BKGND_SET)
        counter += 1
    counter = 0
    for selected_class in game['options'][list(game['options'].keys())[game['cursor_0']]]:
        if counter == game['cursor_1'] and game['cursor_spot'] == 1:
            char_select_console.print(15, counter, selected_class, libtcod.black, libtcod.yellow, bg_blend = libtcod.BKGND_SET)
        else:
            char_select_console.print(15, counter, selected_class, libtcod.white, libtcod.black, bg_blend = libtcod.BKGND_SET)
        counter += 1
    blank_console.print(1, 1, " ", libtcod.black, libtcod.black, libtcod.BKGND_SET)
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(blank_console),
        dest = (
            0,
            0,
            3000,
            3000
        )
    )
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(char_select_console),
        dest = (
            100,
            250,
            char_select_console.width*game['tileset_text'].tile_width,
            char_select_console.height*game['tileset_text'].tile_height
        )
    )
    game['sdl_renderer'].present()


def main_menu(game):
    width = game['console_base'].width
    height = game['console_base'].height

    title_console = libtcod.Console(15, 3)
    title_console.print(x=0, y=0, string="Dragons",  fg=libtcod.red, bg=libtcod.black, bg_blend=libtcod.BKGND_SET, alignment = libtcod.LEFT)
    title_console.print(x=5, y=1, string="are",  fg=libtcod.red, bg=libtcod.black, bg_blend=libtcod.BKGND_SET, alignment = libtcod.LEFT)
    title_console.print(x=6, y=2, string="Dungeons!",  fg=libtcod.red, bg=libtcod.black, bg_blend=libtcod.BKGND_SET, alignment = libtcod.LEFT)

    game['sdl_renderer'].copy(
        game['console_renderer_title'].render(title_console),
        dest = (
            400, 
            100, 
            title_console.width*game['tileset_title'].tile_width, 
            title_console.height*game['tileset_title'].tile_width
    ))

    option_console = libtcod.Console(15, len(game['options']))
    for i, option in enumerate(game['options']):
        if i == game['cursor']:
            fg, bg = (libtcod.black, libtcod.yellow)
        else:
            fg, bg = (libtcod.white, libtcod.black)
        option_console.print(0, i, option, fg, bg, libtcod.BKGND_SET, libtcod.LEFT)

    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(option_console),
        dest = (
            100,
            400,
            option_console.width*game['tileset_text'].tile_width, 
            option_console.height*game['tileset_text'].tile_height)
    )
    

    creator_console = libtcod.Console(10, 1)
    creator_console.print(0, 0, "By: Teggom", libtcod.white, libtcod.black, alignment=libtcod.LEFT)
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(creator_console),
        dest = (
            800,
            400,
            creator_console.width*game['tileset_text'].tile_width,
            creator_console.height*game['tileset_text'].tile_height
        )
    )
    game['sdl_renderer'].present()


def draw_character_stat_menu(chara_height, chara_width, pos_x, pos_y, game):


    if game['cursor_tab'] == 0:
        chara_height = 15
    elif game['cursor_tab'] == 1:
        chara_height = 15
    elif game['cursor_tab'] == 2:
        chara_height = 14
    chara_console= libtcod.Console(chara_width, chara_height)

    skill_box_drop = 0#14
    res_box_drop = 0#28
    chara_console.print_frame(0, 0, chara_width, chara_height, "Character")

    for i, v in enumerate(['Stats', 'Skills', 'Resistances']):
        if game['cursor_tab'] == i:
            chara_console.print(int(chara_width*(i+1)/(game['cursor_tab_options']+1)), 1, v, libtcod.black, libtcod.lighter_gray, alignment=libtcod.CENTER)
        else:    
            chara_console.print(int(chara_width*(i+1)/(game['cursor_tab_options']+1)), 1, v, libtcod.gray, libtcod.darkest_gray, alignment=libtcod.CENTER)

    chara_console.print(chara_console.width-2, 1, "[tab]", libtcod.darker_gray, libtcod.black, alignment=libtcod.RIGHT)

    if game['cursor_tab'] == 0:
        first_indent = 15
        second_indent = 22
        third_indent = 32
        fourth_indent = 46
        fifth_indent = 76

        health_drop = 3
        mana_drop = 4
        p_stat_start_drop = 5
        s_stat_start_drop = 10

        fg = libtcod.black
        bg = libtcod.lighter_gray
        chara_console.print(1, health_drop-1, " "*(chara_width-2), fg, bg)
        chara_console.print(first_indent, health_drop-1, "Stat", fg, bg, alignment=libtcod.RIGHT)
        chara_console.print(second_indent, health_drop-1, "Level", fg, bg, alignment=libtcod.RIGHT)
        chara_console.print(third_indent, health_drop-1, "Equip Bonus", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(fourth_indent, health_drop-1, "Buffs", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(fifth_indent, health_drop-1, "Total", fg, bg, alignment=libtcod.RIGHT)

        for i in range(11):
            if i % 2 == 0:
                bg = libtcod.black
            else:
                bg = libtcod.darkest_gray
            chara_console.print(1, health_drop+i, " "*(chara_width-2), bg=bg)

        (fg, bg) = (libtcod.lighter_gray, libtcod.black)

        indent_1_ops = ['Max Health', 'Max Mana', 'Strength', 'Dexterity', 'Intelligence', "Wisdom", 'Charisma', 'Luck', 'Memory', "Sight", 'Perception']
        for i, v in enumerate(indent_1_ops):
            chara_console.print(first_indent, health_drop + i, v, fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        
        indent_2_ops = [str(game['player'].stats.base_hp), str(game['player'].stats.base_mp), str(game['player'].stats.base_strength),
                        str(game['player'].stats.base_dexterity), str(game['player'].stats.base_intelligence), str(game['player'].stats.base_wisdom),
                        str(game['player'].stats.base_charisma), str(game['player'].stats.base_luck), str(game['player'].stats.base_memory), 
                        str(game['player'].stats.base_sight), str(game['player'].stats.base_perception)]
        for i, v in enumerate(indent_2_ops):
            chara_console.print(second_indent, health_drop + i, v, fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        
        indent_3_ops = [str(game['player'].stats.check_equipment("hp")), 
                        str(game['player'].stats.check_equipment("mp")),
                        str(game['player'].stats.check_equipment("strength")),
                        str(game['player'].stats.check_equipment("dexterity")),
                        str(game['player'].stats.check_equipment("intelligence")),
                        str(game['player'].stats.check_equipment("wisdom")),
                        str(game['player'].stats.check_equipment("charisma")),
                        str(game['player'].stats.check_equipment("luck")),
                        str(game['player'].stats.check_equipment("memory")),
                        str(game['player'].stats.check_equipment("sight")),
                        str(game['player'].stats.check_equipment("perception"))]
        for i, v in enumerate(indent_3_ops):
            chara_console.print(third_indent, health_drop + i, v, fg, bg, libtcod.BKGND_ADD, libtcod.LEFT)

        indent_4_ops = [
            str(game['player'].stats.check_condition("hp")+game['player'].stats.check_traits("hp")),
            str(game['player'].stats.check_condition("mp")+game['player'].stats.check_traits("mp")),
            str(game['player'].stats.check_condition("strength")+game['player'].stats.check_traits("strength")),
            str(game['player'].stats.check_condition("dexterity")+game['player'].stats.check_traits("dexterity")),
            str(game['player'].stats.check_condition("intelligence")+game['player'].stats.check_traits("intelligence")),
            str(game['player'].stats.check_condition("wisdom")+game['player'].stats.check_traits("wisdom")),
            str(game['player'].stats.check_condition("charisma")+game['player'].stats.check_traits("charisma")),
            str(game['player'].stats.check_condition("luck")+game['player'].stats.check_traits("luck")),
            str(game['player'].stats.check_condition("memory")+game['player'].stats.check_traits("memory")),
            str(game['player'].stats.check_condition("sight")+game['player'].stats.check_traits("sight")),
            str(game['player'].stats.check_condition("perception")+game['player'].stats.check_traits("perception"))
        ]
        for i, v in enumerate(indent_4_ops):
            chara_console.print(fourth_indent, health_drop + i, v, fg, bg, libtcod.BKGND_ADD, libtcod.LEFT)
        
        

        indent_5_ops = [
            str(game['player'].stats.hp), str(game['player'].stats.mp), str(game['player'].stats.strength),
            str(game['player'].stats.dexterity), str(game['player'].stats.intelligence), str(game['player'].stats.wisdom),
            str(game['player'].stats.charisma), str(game['player'].stats.luck), str(game['player'].stats.memory),
            str(game['player'].stats.sight), str(game['player'].stats.perception)
        ]
        for i, v in enumerate(indent_5_ops):
            chara_console.print(fifth_indent, health_drop + i, v, fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)


    elif game['cursor_tab'] == 1:
        skill_first_indent = 15
        skill_second_indent = 22
        skill_third_indent = 25
        skill_fourth_indent = 32
        skill_fifth_indent = 46
        skill_sixth_indent = 54
        skill_seventh_indent = 76
        skill_start_drop = skill_box_drop+3

        (fg, bg) = (libtcod.black, libtcod.lighter_gray)

        chara_console.print(1, skill_start_drop-1, " "*(chara_width-2), fg, bg, alignment=libtcod.LEFT)
        chara_console.print(skill_first_indent, skill_start_drop-1, "Skill", fg, bg, alignment=libtcod.RIGHT)
        chara_console.print(skill_second_indent, skill_start_drop-1, "Level", fg, bg, alignment=libtcod.RIGHT)
        chara_console.print(skill_third_indent, skill_start_drop-1, "(Bonus)", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(skill_fourth_indent, skill_start_drop-1, "Equip Bonus", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(skill_fifth_indent, skill_start_drop-1, "Buffs", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(skill_sixth_indent, skill_start_drop-1, "Stat Bonus", fg, bg, alignment=libtcod.LEFT)
        chara_console.print(skill_seventh_indent, skill_start_drop-1, "Total Bonus", fg, bg, alignment=libtcod.RIGHT)

        for i in range(11):
            if i % 2 == 0:
                bg = libtcod.black
            else:
                bg = libtcod.darkest_gray
            chara_console.print(1, skill_start_drop+i, " "*(chara_width-2), bg=bg)

        (fg, bg) = (libtcod.lighter_gray, libtcod.black)
        raw_ops = [
            'athletics',
            'acrobatics',
            'slight_of_hand',
            'stealth',
            'arcana',
            'alchemy',
            'crafting',
            'bartering',
            'persuasion',
            'intimidation',
            'deception'
        ]
        ops = [
            'Athletics',
            'Acrobatics',
            'Slight of Hand',
            "Stealth",
            "Arcana",
            'Alchemy',
            "Crafting",
            'Bartering',
            "Persuasion",
            'Intimidation',
            "Deception"
        ]
        for i, v in enumerate(ops):
            chara_console.print(skill_first_indent, skill_start_drop+i, v, fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(skill_second_indent, skill_start_drop+i, str(game['player'].stats.level_tracker.levels[raw_ops[i]]['level']), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(skill_third_indent, skill_start_drop+i, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels[raw_ops[i]]['level'])), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT)
            chara_console.print(skill_fourth_indent, skill_start_drop+i, str(game['player'].stats.skill_check_equipment(raw_ops[i])), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT)
            chara_console.print(skill_fifth_indent, skill_start_drop+i, str(game['player'].stats.skill_check_condition(raw_ops[i])+game['player'].stats.skill_check_traits(raw_ops[i])), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT)
            
        chara_console.print(skill_sixth_indent, skill_start_drop+0, str(game['player'].stats.get_skill_mod(int(game['player'].stats.strength))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # athletics
        chara_console.print(skill_sixth_indent, skill_start_drop+1, str(game['player'].stats.get_skill_mod(int(game['player'].stats.strength*.5) + int(game['player'].stats.dexterity*.5))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # acrobatics
        chara_console.print(skill_sixth_indent, skill_start_drop+2, str(game['player'].stats.get_skill_mod(int(game['player'].stats.dexterity))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # slight_of_hand 
        chara_console.print(skill_sixth_indent, skill_start_drop+3, str(game['player'].stats.get_skill_mod(int(game['player'].stats.dexterity*.75) + int(game['player'].stats.wisdom*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # stealth 
        chara_console.print(skill_sixth_indent, skill_start_drop+4, str(game['player'].stats.get_skill_mod(int(game['player'].stats.intelligence))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # arcana 
        chara_console.print(skill_sixth_indent, skill_start_drop+5, str(game['player'].stats.get_skill_mod(int(game['player'].stats.intelligence*.75) + int(game['player'].stats.wisdom*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # alchemy 
        chara_console.print(skill_sixth_indent, skill_start_drop+6, str(game['player'].stats.get_skill_mod(int(game['player'].stats.wisdom*.75) + int(game['player'].stats.dexterity*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # crafting
        chara_console.print(skill_sixth_indent, skill_start_drop+7, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # bartering
        chara_console.print(skill_sixth_indent, skill_start_drop+8, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.wisdom*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # persuasion 
        chara_console.print(skill_sixth_indent, skill_start_drop+9, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.strength*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # intimidation 
        chara_console.print(skill_sixth_indent, skill_start_drop+10, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.intelligence*.25))), fg, bg, libtcod.BKGND_ADD, libtcod.LEFT) # deception

        chara_console.print(skill_seventh_indent, skill_start_drop+0, str(game['player'].stats.athletics), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+1, str(game['player'].stats.acrobatics), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+2, str(game['player'].stats.slight_of_hand), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+3, str(game['player'].stats.stealth), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+4, str(game['player'].stats.arcana), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+5, str(game['player'].stats.alchemy), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+6, str(game['player'].stats.crafting), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+7, str(game['player'].stats.bartering), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+8, str(game['player'].stats.persuasion), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+9, str(game['player'].stats.intimidation), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        chara_console.print(skill_seventh_indent, skill_start_drop+10, str(game['player'].stats.deception), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
        
    elif game['cursor_tab'] == 2:
        res_drop = res_box_drop + 3
        for i in range(10):
            if i % 2 == 0:
                bg = libtcod.black
            else:
                bg = libtcod.darkest_gray
            chara_console.print(1, res_drop + i, ' '*(chara_width-2), bg=bg)

        res_first_indent = 15
        res_second_indent = 22
        res_third_indent = 32
        res_fourth_indent = 46
        res_fifth_indent = 54
        res_sixth_indent = 76
        #skill_sixth_indent = 54
        #skill_seventh_indent = 76
        #skill_start_drop = skill_box_drop+3

        (fg, bg) = (libtcod.black, libtcod.lighter_gray)

        chara_console.print(1, res_drop-1, " "*(chara_width-4), fg, bg)
        chara_console.print(res_first_indent, res_drop-1, "Resistance", fg, bg, libtcod.BKGND_SET, libtcod.RIGHT)
        chara_console.print(res_second_indent, res_drop-1, "Base", fg, bg, libtcod.BKGND_SET, libtcod.RIGHT)
        chara_console.print(res_third_indent, res_drop-1, "Equip Bonus", fg, bg, libtcod.BKGND_SET, libtcod.LEFT)
        chara_console.print(res_fourth_indent, res_drop-1, "Buffs", fg, bg, libtcod.BKGND_SET, libtcod.LEFT)
        chara_console.print(res_fifth_indent, res_drop-1, "Total", fg, bg, libtcod.BKGND_SET, libtcod.LEFT)
        chara_console.print(res_sixth_indent, res_drop-1, "Dmg % Taken", fg, bg, libtcod.BKGND_SET, libtcod.RIGHT)

        ops = [
            'Slash Resist',
            'Pierce Resist',
            'Blunt Resist',
            'Fire Resist',
            'Frost Resist',
            'Shock Resist',
            'Arcane Resist',
            'Poison Resist',
            'Holy Resist',
            'Unholy Resist'
        ]
        raw_ops = [
            'slash',
            'pierce',
            'blunt',
            'fire',
            'frost',
            'shock',
            'arcane',
            'poison',
            'holy',
            'unholy'
        ]
        (fg, bg) = (libtcod.lighter_gray, libtcod.black)

        # wised up and used raw_ops here 
        for i, v in enumerate(raw_ops):
            chara_console.print(res_first_indent, res_drop+i, ops[i], fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(res_second_indent, res_drop+i, str(game['player'].stats.resistances.get_resistance(v, False, ['base'])), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(res_third_indent, res_drop+i, str(game['player'].stats.resistances.get_resistance(v, False, ['equip'])), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(res_fourth_indent, res_drop+i, str(game['player'].stats.resistances.get_resistance(v, False, ['traits', 'conditions'])), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(res_fifth_indent, res_drop+i, str(game['player'].stats.resistances.get_resistance(v, False)), fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)
            chara_console.print(res_sixth_indent, res_drop+i, str(int(100*round(game['player'].stats.resistances.get_resistance(v), 2)))+" %", fg, bg, libtcod.BKGND_ADD, libtcod.RIGHT)

        
    game['sdl_renderer'].copy(
        game['console_renderer_text'].render(chara_console),
        dest = (
            pos_x,
            pos_y,
            chara_console.width*game['tileset_text'].tile_width,
            chara_console.height*game['tileset_text'].tile_height
        )
    )
