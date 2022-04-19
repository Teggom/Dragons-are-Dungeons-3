import enum
import math
import tcod as libtcod
from textwrap import wrap
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


    libtcod.console_blit(slot_window, -1, -2, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    # BAG
    using_bag = game['player'].inventory.bag[gear_lookup(game['slot_names'][game['cursor_0']])]
    #bag_height = min(14, max(len(using_bag)+2, 3))
    bag_height = 14
    # if using_bag == []:
    #     bag_width = len(NO_EQUIP) + 3
    # else:
    #     bag_width = max([len(x.q_name) for x in using_bag]) + 5
    bag_width = 34
    bag_window = libtcod.console_new(bag_width, bag_height)
    libtcod.console_print_frame(bag_window, 0, 0, bag_width, bag_height, True, fmt=gear_lookup(game['slot_names'][game['cursor_0']]))


    if len(using_bag) == 0:
        libtcod.console_set_default_foreground(bag_window, libtcod.dark_gray)
        libtcod.console_set_default_background(bag_window, libtcod.black)
        libtcod.console_print_ex(bag_window, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, NO_EQUIP)
    else:
        page = int(game['cursor_1']/(bag_height-2))
        #print(page*(bag_height-2), page+1*(bag_height-2))
        for i, v in enumerate(using_bag):
            if i >= page*(bag_height-2) and i < (page+1)*(bag_height-2):                    
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
                libtcod.console_print_ex(bag_window, 1, i+1-page*(bag_height-2), libtcod.BKGND_SET, libtcod.LEFT, v.q_name+r_padding*" ")
        libtcod.console_set_default_foreground(bag_window, libtcod.black)
        libtcod.console_set_default_background(bag_window, libtcod.lighter_gray)
        libtcod.console_print_ex(bag_window, bag_width-2, bag_height-1, libtcod.BKGND_SET, libtcod.RIGHT, "page {}/{}".format(page+1, int(1+len(using_bag)/bag_height)))
            
    # puts it under the main window
    #libtcod.console_blit(bag_window, 0, -15, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)
    # puts it to the right of the main window
    libtcod.console_blit(bag_window, -slot_width-2, -2, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    chara_height = 30
    chara_width = 80
    chara_window = libtcod.console_new(chara_width, chara_height)

    skill_box_drop = 14

    libtcod.console_print_frame(chara_window, 0, 0, chara_width, chara_height, True, fmt="Character")
    libtcod.console_print_frame(chara_window, 1, 1, chara_width-2, skill_box_drop, True)
    libtcod.console_print_frame(chara_window, 1, skill_box_drop+1, chara_width-2, chara_height-skill_box_drop-2, True)


    first_indent = 15
    second_indent = 22
    third_indent = 32
    fourth_indent = 46
    fifth_indent = 76

    health_drop = 3
    mana_drop = 4
    p_stat_start_drop = 5
    s_stat_start_drop = 10



    libtcod.console_set_default_foreground(chara_window, libtcod.black)
    libtcod.console_set_default_background(chara_window, libtcod.lighter_gray)

    libtcod.console_print_ex(chara_window, 2, health_drop-1, libtcod.BKGND_SET, libtcod.LEFT, " "*(chara_width-4))
    libtcod.console_print_ex(chara_window, first_indent, health_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Stat")
    libtcod.console_print_ex(chara_window, second_indent, health_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Level")
    libtcod.console_print_ex(chara_window, third_indent, health_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "Equip Bonus")
    libtcod.console_print_ex(chara_window, fourth_indent, health_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "Buffs")
    libtcod.console_print_ex(chara_window, fifth_indent, health_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Total")
    
    for i in range(11):
        if i % 2 == 0:
            libtcod.console_set_default_background(chara_window, libtcod.black)
        else:
            libtcod.console_set_default_background(chara_window, libtcod.darkest_gray) 
        libtcod.console_print_ex(chara_window, 2, health_drop+i, libtcod.BKGND_SET, libtcod.LEFT, ' '*(chara_width-4))

    libtcod.console_set_default_foreground(chara_window, libtcod.lighter_gray)
    libtcod.console_set_default_background(chara_window, libtcod.black)

    
    # To_Print_1 = ['Max Health', 'Max Mana', "Strength", "Dexterity", "Intelligence", "Wisdom", "Charisma", "Luck", "Memory", "Sight", "Perception"]
    # for i, v in enumerate(To_Print_1):
    #     if i % 2 == 0:
    #         libtcod.console_set_default_background(chara_window, libtcod.black)
    #     else:
    #         libtcod.console_set_default_background(chara_window, libtcod.darkest_gray) 
    #     libtcod.console_print_ex(chara_window, first_indent, health_drop+i, libtcod.BKGND_SET, libtcod.RIGHT, v)

    libtcod.console_print_ex(chara_window, first_indent, health_drop, libtcod.BKGND_ADD, libtcod.RIGHT, "Max Health")
    libtcod.console_print_ex(chara_window, first_indent, mana_drop, libtcod.BKGND_ADD, libtcod.RIGHT, "Max Mana")
    libtcod.console_print_ex(chara_window, first_indent, p_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, "Strength")
    libtcod.console_print_ex(chara_window, first_indent, p_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, "Dexterity")
    libtcod.console_print_ex(chara_window, first_indent, p_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, "Intelligence")
    libtcod.console_print_ex(chara_window, first_indent, p_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, "Wisdom")
    libtcod.console_print_ex(chara_window, first_indent, p_stat_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, "Charisma")
    libtcod.console_print_ex(chara_window, first_indent, s_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, "Luck")
    libtcod.console_print_ex(chara_window, first_indent, s_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, "Memory")
    libtcod.console_print_ex(chara_window, first_indent, s_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, "Sight")
    libtcod.console_print_ex(chara_window, first_indent, s_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, "Perception")

    libtcod.console_print_ex(chara_window, second_indent, health_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_hp))
    libtcod.console_print_ex(chara_window, second_indent, mana_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_mp))
    libtcod.console_print_ex(chara_window, second_indent, p_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_strength))
    libtcod.console_print_ex(chara_window, second_indent, p_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_dexterity))
    libtcod.console_print_ex(chara_window, second_indent, p_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_intelligence))
    libtcod.console_print_ex(chara_window, second_indent, p_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_wisdom))
    libtcod.console_print_ex(chara_window, second_indent, p_stat_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_charisma))
    libtcod.console_print_ex(chara_window, second_indent, s_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_luck))
    libtcod.console_print_ex(chara_window, second_indent, s_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_memory))
    libtcod.console_print_ex(chara_window, second_indent, s_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_sight))
    libtcod.console_print_ex(chara_window, second_indent, s_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.base_perception))

    
    libtcod.console_print_ex(chara_window, third_indent, health_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("hp")))
    libtcod.console_print_ex(chara_window, third_indent, mana_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("mp")))
    libtcod.console_print_ex(chara_window, third_indent, p_stat_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("strength")))
    libtcod.console_print_ex(chara_window, third_indent, p_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("dexterity")))
    libtcod.console_print_ex(chara_window, third_indent, p_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("intelligence")))
    libtcod.console_print_ex(chara_window, third_indent, p_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("wisdom")))
    libtcod.console_print_ex(chara_window, third_indent, p_stat_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("charisma")))
    libtcod.console_print_ex(chara_window, third_indent, s_stat_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("luck")))
    libtcod.console_print_ex(chara_window, third_indent, s_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("memory")))
    libtcod.console_print_ex(chara_window, third_indent, s_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("sight")))
    libtcod.console_print_ex(chara_window, third_indent, s_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_equipment("perception")))

    
    libtcod.console_print_ex(chara_window, fourth_indent, health_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("hp")+game['player'].stats.check_traits("hp")))
    libtcod.console_print_ex(chara_window, fourth_indent, mana_drop, libtcod.BKGND_ADD, libtcod.LEFT,  str(game['player'].stats.check_condition("mp")+game['player'].stats.check_traits("mp")))
    libtcod.console_print_ex(chara_window, fourth_indent, p_stat_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("strength")+game['player'].stats.check_traits("strength")))
    libtcod.console_print_ex(chara_window, fourth_indent, p_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("dexterity")+game['player'].stats.check_traits("dexterity")))
    libtcod.console_print_ex(chara_window, fourth_indent, p_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("intelligence")+game['player'].stats.check_traits("intelligence")))
    libtcod.console_print_ex(chara_window, fourth_indent, p_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("wisdom")+game['player'].stats.check_traits("wisdom")))
    libtcod.console_print_ex(chara_window, fourth_indent, p_stat_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("charisma")+game['player'].stats.check_traits("charisma")))
    libtcod.console_print_ex(chara_window, fourth_indent, s_stat_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("luck")+game['player'].stats.check_traits("luck")))
    libtcod.console_print_ex(chara_window, fourth_indent, s_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("memory")+game['player'].stats.check_traits("memory")))
    libtcod.console_print_ex(chara_window, fourth_indent, s_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("sight")+game['player'].stats.check_traits("sight")))
    libtcod.console_print_ex(chara_window, fourth_indent, s_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.check_condition("perception")+game['player'].stats.check_traits("perception")))
    #libtcod.console_print_ex(chara_window, 5, 5, libtcod.BKGND_SET, libtcod.LEFT, "Strength")

    libtcod.console_print_ex(chara_window, fifth_indent, health_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.hp))
    libtcod.console_print_ex(chara_window, fifth_indent, mana_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.mp))
    libtcod.console_print_ex(chara_window, fifth_indent, p_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.strength))
    libtcod.console_print_ex(chara_window, fifth_indent, p_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.dexterity))
    libtcod.console_print_ex(chara_window, fifth_indent, p_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.intelligence))
    libtcod.console_print_ex(chara_window, fifth_indent, p_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.wisdom))
    libtcod.console_print_ex(chara_window, fifth_indent, p_stat_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.charisma))
    libtcod.console_print_ex(chara_window, fifth_indent, s_stat_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.luck))
    libtcod.console_print_ex(chara_window, fifth_indent, s_stat_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.memory))
    libtcod.console_print_ex(chara_window, fifth_indent, s_stat_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.sight))
    libtcod.console_print_ex(chara_window, fifth_indent, s_stat_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.perception))



    
    skill_first_indent = 15
    skill_second_indent = 22
    skill_third_indent = 25
    skill_fourth_indent = 32
    skill_fifth_indent = 46
    skill_sixth_indent = 54
    skill_seventh_indent = 76
    skill_start_drop = skill_box_drop+3

    libtcod.console_set_default_foreground(chara_window, libtcod.black)
    libtcod.console_set_default_background(chara_window, libtcod.lighter_gray)

    libtcod.console_print_ex(chara_window, 2, skill_start_drop-1, libtcod.BKGND_SET, libtcod.LEFT, " "*(chara_width-4))
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Skill")
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Level")
    libtcod.console_print_ex(chara_window, skill_third_indent-1, skill_start_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "(Bonus)")
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "Equip Bonus")
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "Buffs")
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.LEFT, "Stat Bonus")
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop-1, libtcod.BKGND_SET, libtcod.RIGHT, "Total Bonus")

    for i in range(11):
        if i % 2 == 0:
            libtcod.console_set_default_background(chara_window, libtcod.black)
        else:
            libtcod.console_set_default_background(chara_window, libtcod.darkest_gray) 
        libtcod.console_print_ex(chara_window, 2, skill_start_drop+i, libtcod.BKGND_SET, libtcod.LEFT, ' '*(chara_width-4))

    libtcod.console_set_default_foreground(chara_window, libtcod.lighter_gray)
    libtcod.console_set_default_background(chara_window, libtcod.black)

    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, "Athletics")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, "Acrobatics")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, "Slight of Hand")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, "Stealth")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, "Arcana")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.RIGHT, "Alchemy")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.RIGHT, "Crafting")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.RIGHT, "Bartering")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.RIGHT, "Persuasion")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.RIGHT, "Intimidation")
    libtcod.console_print_ex(chara_window, skill_first_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.RIGHT, "Deception")

    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['athletics']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['acrobatics']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['slight_of_hand']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['stealth']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['arcana']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['alchemy']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['crafting']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['bartering']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['persuasion']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['intimidation']['level']))
    libtcod.console_print_ex(chara_window, skill_second_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.level_tracker.levels['deception']['level']))

    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['athletics']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['acrobatics']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['slight_of_hand']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['stealth']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['arcana']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['alchemy']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['crafting']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['bartering']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['persuasion']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['intimidation']['level'])))
    libtcod.console_print_ex(chara_window, skill_third_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_level_to_bonus(game['player'].stats.level_tracker.levels['deception']['level'])))
    
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("athletics")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("acrobatics")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("slight_of_hand")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("stealth")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("arcana")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("alchemy")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("crafting")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("bartering")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("persuasion")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("intimidation")))
    libtcod.console_print_ex(chara_window, skill_fourth_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_equipment("deception")))
    
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("athletics")+game['player'].stats.skill_check_traits("athletics")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("acrobatics")+game['player'].stats.skill_check_traits("acrobatics")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("slight_of_hand")+game['player'].stats.skill_check_traits("slight_of_hand")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("stealth")+game['player'].stats.skill_check_traits("stealth")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("arcana")+game['player'].stats.skill_check_traits("arcana")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("alchemy")+game['player'].stats.skill_check_traits("alchemy")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("crafting")+game['player'].stats.skill_check_traits("crafting")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("bartering")+game['player'].stats.skill_check_traits("bartering")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("persuasion")+game['player'].stats.skill_check_traits("persuasion")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("intimidation")+game['player'].stats.skill_check_traits("intimidation")))
    libtcod.console_print_ex(chara_window, skill_fifth_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.skill_check_condition("deception")+game['player'].stats.skill_check_traits("deception")))
    
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.strength)))) # athletics
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.strength*.5) + int(game['player'].stats.dexterity*.5)))) # acrobatics
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.dexterity))))# slight_of_hand 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.dexterity*.75) + int(game['player'].stats.wisdom*.25)))) # stealth 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.intelligence))))# arcana 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.intelligence*.75) + int(game['player'].stats.wisdom*.25))))# alchemy 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.wisdom*.75) + int(game['player'].stats.dexterity*.25))))# crafting
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma))))# bartering
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.wisdom*.25))))# persuasion 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.strength*.25))))# intimidation 
    libtcod.console_print_ex(chara_window, skill_sixth_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.LEFT, str(game['player'].stats.get_skill_mod(int(game['player'].stats.charisma*.75) + int(game['player'].stats.intelligence*.25))))# deception
    
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.athletics))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+1, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.acrobatics))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+2, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.slight_of_hand))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+3, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.stealth))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+4, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.arcana))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+5, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.alchemy))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+6, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.crafting))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+7, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.bartering))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+8, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.persuasion))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+9, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.intimidation))
    libtcod.console_print_ex(chara_window, skill_seventh_indent, skill_start_drop+10, libtcod.BKGND_ADD, libtcod.RIGHT, str(game['player'].stats.deception))
    libtcod.console_blit(chara_window, -1, -17, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    item_height = 45
    item_width = 45
    item_window = libtcod.console_new(item_width, item_height)
    libtcod.console_print_frame(item_window, 0, 0, item_width, item_height, True, fmt="Item")
    text_indent = 15
    old_value_indent = 17
    arrow_indent = 21
    new_value_indent = 25
    s_drop = 3
    stat_drop = s_drop+4
    skill_drop = stat_drop+10
    resistance_drop = skill_drop + 12

    
    libtcod.console_set_default_foreground(item_window, libtcod.black)
    libtcod.console_set_default_background(item_window, libtcod.lighter_gray)
    
    for i in range(item_height-3):
        if i % 2 == 0:
            libtcod.console_set_default_background(item_window, libtcod.black)
        else:
            libtcod.console_set_default_background(item_window, libtcod.darkest_gray) 
        libtcod.console_print_ex(item_window, 1, i+2, libtcod.BKGND_ADD, libtcod.LEFT, ' '*(item_width-2))

    libtcod.console_set_default_foreground(item_window, libtcod.lighter_gray)
    libtcod.console_set_default_background(item_window, libtcod.black)

    if game['cursor_spot'] == 0:
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
        else:
            item = None
    else:
        item = using_bag[game['cursor_1']]
    
    if item:
        name = wrap(item.name, item_width-2)
        libtcod.console_print_ex(item_window, int(item_width/2), 1, libtcod.BKGND_NONE, libtcod.CENTER, name[0])
        if len(name) == 2:
            libtcod.console_print_ex(item_window, int(item_width/2), 2, libtcod.BKGND_NONE, libtcod.CENTER, name[1])
        
        libtcod.console_print_ex(item_window, text_indent, s_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Rarity:")
        libtcod.console_print_ex(item_window, new_value_indent, s_drop, libtcod.BKGND_NONE, libtcod.LEFT, "TODO")
        
        libtcod.console_print_ex(item_window, text_indent, s_drop+1, libtcod.BKGND_NONE, libtcod.RIGHT, "Value:")
        libtcod.console_print_ex(item_window, new_value_indent, s_drop+1, libtcod.BKGND_NONE, libtcod.LEFT, "TODO")
        
        libtcod.console_print_ex(item_window, text_indent, s_drop+2, libtcod.BKGND_NONE, libtcod.RIGHT, "Type:")
        libtcod.console_print_ex(item_window, new_value_indent, s_drop+2, libtcod.BKGND_NONE, libtcod.LEFT, item.type)
        
        libtcod.console_set_default_foreground(chara_window, libtcod.lighter_yellow)



        base_color = libtcod.lighter_gray
        decrease_color = libtcod.red
        same_color = libtcod.darker_gray
        increase_color = libtcod.green

        header_fore = libtcod.black
        header_back = libtcod.gray
        # MAKE
        # in green
        # Strength: 20 -> 23   (+3)
        # in red
        #   Wisdom: 20 -> 0    (-20)
        # in gray
        # Charisma: 13 -> 13   (0)
        

        libtcod.console_set_default_foreground(item_window, header_fore)
        libtcod.console_set_default_background(item_window, header_back)
        libtcod.console_print_ex(item_window, arrow_indent, stat_drop-1, libtcod.BKGND_SET, libtcod.CENTER, "STATS")

        cur_stat = "strength"
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Strength:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Strength:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        
        cur_stat = "dexterity"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Dexterity:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Dexterity:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "intelligence"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Intelligence:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Intelligence:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "wisdom"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Wisdom:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Wisdom:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "charisma"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Charisma:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Charisma:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "luck"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Luck:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Luck:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "memory"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Memory:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Memory:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "sight"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Sight:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Sight:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_stat = "perception"
        stat_drop += 1
        new_stat = 0
        if item.stats.get(cur_stat):
            new_stat += item.stats.get(cur_stat)
        if item.traits.get(cur_stat):
            new_stat += item.traits.get(cur_stat)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_stat):
                old_stat += old_item.stats.get(cur_stat)
            if old_item.traits.get(cur_stat):
                old_stat += old_item.traits.get(cur_stat)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Perception:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Perception:")
            libtcod.console_print_ex(item_window, arrow_indent, stat_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, stat_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        libtcod.console_set_default_foreground(item_window, header_fore)
        libtcod.console_set_default_background(item_window, header_back)
        libtcod.console_print_ex(item_window, arrow_indent, skill_drop-1, libtcod.BKGND_SET, libtcod.CENTER, "SKILLS")


        cur_skill = "athletics"
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Athletics:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Athletics:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "acrobatics"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Acrobatics:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Acrobatics:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "slight_of_hand"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Slight of Hand:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Slight of Hand:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "stealth"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Stealth:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Stealth:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "arcana"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Arcana:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Arcana:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "alchemy"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Alchemy:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Alchemy:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "crafting"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Crafting:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Crafting:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "bartering"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Bartering:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Bartering:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "persuasion"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Persuasion:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Persuasion:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "intimidation"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Intimidation:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Intimidation:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        cur_skill = "deception"
        skill_drop += 1
        new_stat = 0
        if item.stats.get(cur_skill):
            new_stat += item.stats.get(cur_skill)
        if item.traits.get(cur_skill):
            new_stat += item.traits.get(cur_skill)
        old_stat = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.stats.get(cur_skill):
                old_stat += old_item.stats.get(cur_skill)
            if old_item.traits.get(cur_skill):
                old_stat += old_item.traits.get(cur_skill)
        
        if game['cursor_spot'] == 0:
            if new_stat == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Deception:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_stat == old_stat:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Deception:")
            libtcod.console_print_ex(item_window, arrow_indent, skill_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_stat))
            if old_stat > new_stat:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_stat < new_stat:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, skill_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_stat))
        
        libtcod.console_set_default_foreground(item_window, header_fore)
        libtcod.console_set_default_background(item_window, header_back)
        libtcod.console_print_ex(item_window, arrow_indent, resistance_drop-1, libtcod.BKGND_SET, libtcod.CENTER, "RESISTANCES")

        
        cur_res = "slash"
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Slash Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Slash Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        

        cur_res = "pierce"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Pierce Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Pierce Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        
        cur_res = "blunt"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Blunt Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Blunt Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        

        cur_res = "fire"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Fire Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Fire Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        cur_res = "frost"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Frost Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Frost Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        cur_res = "shock"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Shock Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Shock Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        cur_res = "arcane"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Arcane Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Arcane Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        cur_res = "poison"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Poison Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Poison Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        cur_res = "holy"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Holy Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Holy Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        
        cur_res = "unholy"
        resistance_drop += 1
        new_res = 0
        if item.resistances.get(cur_res + "_resistance"):
            new_res += item.resistances.get(cur_res + "_resistance")
        if item.traits.get(cur_res + "_resistance"):
            new_res += item.traits.get(cur_res + "_resistance")
        old_res = 0
        if game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]:
            old_item = game['player'].inventory.wearing[game['slot_names'][game['cursor_0']]]
            if old_item.resistances.get(cur_res + "_resistance"):
                old_res += old_item.resistances.get(cur_res + "_resistance")
            if old_item.traits.get(cur_res + "_resistance"):
                old_res += old_item.traits.get(cur_res + "_resistance")
        if game['cursor_spot'] == 0:
            if new_res == 0:
                libtcod.console_set_default_foreground(item_window, same_color)
            else:
                libtcod.console_set_default_foreground(item_window, base_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Unholy Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))

        else:
            libtcod.console_set_default_foreground(item_window, base_color)
            if new_res == old_res:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, text_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "Unholy Resist:")
            libtcod.console_print_ex(item_window, arrow_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.RIGHT, "->")
            libtcod.console_print_ex(item_window, old_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(old_res))
            if old_res > new_res:
                libtcod.console_set_default_foreground(item_window, decrease_color)
            elif old_res < new_res:
                libtcod.console_set_default_foreground(item_window, increase_color)
            else:
                libtcod.console_set_default_foreground(item_window, same_color)
            libtcod.console_print_ex(item_window, new_value_indent, resistance_drop, libtcod.BKGND_NONE, libtcod.LEFT, str(new_res))
        

    libtcod.console_blit(item_window, -bag_width-slot_width-3, -2, game['screen_width'], game['screen_height'], 0, 0, 0, 1.0, 0.7)

    pass

def ground_menu(con, game, items):
    height = 15 #len(items) + 5
    width = 33
    #for item in items:
    #    width = max(width, 9+len(item.name)+len(item.type))
    #print(width)
    window = libtcod.console_new(width, height)
    libtcod.console_print_frame(window, 0, 0, width, height, True, fmt="Ground")
    #libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Ground Items")
    if len(items) == 0:
        libtcod.console_set_default_foreground(window, libtcod.dark_gray)
        libtcod.console_print_ex(window, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "nothing here...")
    else:
        page = int(game['cursor']/(height-2))
        for i, v in enumerate(items):
            if i >= page*(height-2) and i < (page+1)*(height-2):
                text = ""
                if game['cursor'] == i:
                    libtcod.console_set_default_foreground(window, libtcod.black)
                    libtcod.console_set_default_background(window, libtcod.lighter_yellow)
                else:
                    libtcod.console_set_default_foreground(window, libtcod.gray)
                    libtcod.console_set_default_background(window, libtcod.black)
                text += v.name
                libtcod.console_print_ex(window, 1, i+1-page*(height-2), libtcod.BKGND_SET, libtcod.LEFT, text)
        libtcod.console_set_default_foreground(window, libtcod.black)
        libtcod.console_set_default_background(window, libtcod.lighter_gray)
        libtcod.console_print_ex(window, width-2, height-1, libtcod.BKGND_SET, libtcod.RIGHT, "page {}/{}".format(page+1, int(1+len(items)/height)))
        

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
