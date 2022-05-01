from unittest.mock import NonCallableMagicMock
from bundled.traits_loader import trait_generator
from unit_components.item import Item
from unit_components.damage import Damage
from entity import Entity
from random import sample
import tcod as libtcod


class item_generator():
    def __init__(self, game):
        self.items_generated = 0
        self.tiles = game['TILES']
        self.items = ['iron_helm', 'iron_necklace', "iron_chestplate", "iron_chain_cloak", "iron_gauntlet", "iron_sword", "iron_dagger", "iron_hammer", "iron_axe", "iron_ring", "iron_belt", "iron_leggings", "iron_shoe"]
    
    def generate(self, name):
        if name == "iron_helm":
            new_item = Item(
                name =              "Iron Helm",
                type =              "Head",
                vis_package =       self.tiles['HELMET'],
                noise =             2,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"slash_resistance" : 3, 'blunt_resistance' : 2, "pierce_resistance" : 3},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_necklace":
            new_item = Item(
                name =              "Iron Necklace",
                type =              "Neck",
                vis_package =       self.tiles['NECK'],
                noise =             1,
                trait =             None,
                conditions =        [],
                stats =             {"luck" : 1},
                skills =            {},
                resistances =       {"arcane_resistance" : 5, "frost_resistance" : -1},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_chestplate":
            new_item = Item(
                name =              "Iron Chestplate",
                type =              "Chest",
                vis_package =       self.tiles['CHEST'],
                noise =             10,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"frost_resistance" : -3, "fire_resistance" : -3, 'shock_resistance' : -5, 'arcane_resistance' : 1, "blunt_resistance" : 10, "slash_resistance" : 10, "pierce_resistance" : 10},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_chain_cloak":
            new_item = Item(
                name =              "Chain Iron Cloak",
                type =              "Back",
                vis_package =       self.tiles['BACK'],
                noise =             15,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"blunt_resistance" : 10, "slash_resistance" : 10, "pierce_resistance" : 10},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_gauntlet":
            new_item = Item(
                name =              "Iron Gauntlet",
                type =              "Arm",
                vis_package =       self.tiles['ARM'],
                noise =             3,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"blunt_resistance" : 3, "slash_resistance" : 3, "pierce_resistance" : 3},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_sword":
            new_item = Item(
                name =              "Iron Sword",
                type =              "Weapon",
                vis_package =       self.tiles['SWORD'],
                noise =             3,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {},
                damages =           [Damage("1d6+1", "slash")],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_dagger":
            new_item = Item(
                name =              "Iron Dagger",
                type =              "Weapon",
                vis_package =       self.tiles['DAGGER'],
                noise =             0,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {},
                damages =           [Damage("1d4", "slash"), Damage("1d3", "pierce")],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_hammer":
            new_item = Item(
                name =              "Iron Hammer",
                type =              "Weapon",
                vis_package =       self.tiles['HAMMER'],
                noise =             5,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {},
                damages =           [Damage("1d12", "blunt")],
                twohand =           True,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_axe":
            new_item = Item(
                name =              "Iron Axe",
                type =              "Weapon",
                vis_package =       self.tiles['AXE'],
                noise =             3,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {},
                damages =           [Damage("2d6", "slash")],
                twohand =           True,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_ring":
            new_item = Item(
                name =              "Iron Ring",
                type =              "Rings",
                vis_package =       self.tiles['ARM'],
                noise =             0,
                trait =             None,
                conditions =        [],
                stats =             {"sight" : 2, "luck" : 2},
                skills =            {},
                resistances =       {"holy_resistance" : -4, "unholy_resistance" : 4},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_belt":
            new_item = Item(
                name =              "Iron Belt",
                type =              "Belt",
                vis_package =       self.tiles['BELT'],
                noise =             0,
                trait =             None,
                conditions =        [],
                stats =             {"strength" : 2},
                skills =            {"acrobatics" : 1},
                resistances =       {},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_leggings":
            new_item = Item(
                name =              "Iron Leggings",
                type =              "Legs",
                vis_package =       self.tiles['LEGS'],
                noise =             7,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"slash_resistance" : 3, "blunt_resistance" : 3, "piece_resistance" : 3},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )
        if name == "iron_shoe":
            new_item = Item(
                name =              "Iron Shoe",
                type =              "Feet",
                vis_package =       self.tiles['FEET'],
                noise =             12,
                trait =             None,
                conditions =        [],
                stats =             {},
                skills =            {},
                resistances =       {"slash_resistance" : 2, "blunt_resistance" : 2, "piece_resistance" : 2},
                damages =           [],
                twohand =           False,
                perturn_func =      [],
                peruse_func =       [],
                onhit_enemy_func =  [],
                quantity =          1
            )

        return(new_item)







def make_item(name, game):
    t_gen = trait_generator()
    i_gen = item_generator(game)
    itm_n = sample(i_gen.items, 1)[0]
    trt_0 = sample(t_gen.traits, 1)[0]
    reps = [None, None, None, None, None, None, None, None, None, trt_0]
    trt_n = sample(reps, 1)[0]
    
    itm = i_gen.generate(itm_n)
    if trt_n is not None:
        itm.trait = t_gen.generate(trt_n)
    
    return(itm)
    

def remove_item_from_map(item, game):
    game['items'].remove(item)

def place_item(item, game, x=None, y=None):
    if x == None:
        x = sample(range(game['map_height']), 1)[0]
    if y == None:
        y = sample(range(game['map_width']), 1)[0]
    item.x = x
    item.y = y
    game['items'].append(item)

def ascii_loader():
    ret = {}
    ret['PLAYER'] = {'CHAR' : 1, 'COLOR' : libtcod.white}         # 64
    #ret['PLAYER'] = {'CHAR' : 'ⁿ', 'COLOR' : libtcod.red}       
    ret['NPC'] = {'CHAR' : '☺', 'COLOR' : libtcod.amber}          # 1
    ret['SWORD'] = {'CHAR' : '¬', 'COLOR' : libtcod.red}         # 170
    ret['DAGGER'] = {'CHAR' : '-', "COLOR" : libtcod.gray}
    ret['HAMMER'] = {'CHAR' : 'T', "COLOR" : libtcod.gray}
    ret['AXE'] = {'CHAR' : '°', 'COLOR' : libtcod.gray}           # 248
    ret['HELMET'] = {'CHAR' : '⌐', 'COLOR' : libtcod.gray}        # 169
    ret['NECK'] = {'CHAR' : '♀', 'COLOR' : libtcod.silver}          # 12
    ret['BACK'] = {'CHAR' : '÷', 'COLOR' : libtcod.Color(185, 122, 90)}          # 246
    ret['CHEST'] = {'CHAR' : '≤', 'COLOR' : libtcod.gray}         # 243
    ret['ARM'] = {'CHAR' : '≥', 'COLOR' : libtcod.Color(185, 122, 90)}           # 242
    ret['BELT'] = {'CHAR' : 'ε', 'COLOR' : libtcod.Color(185, 122, 90)}            # 238
    ret['RING'] = {'CHAR' : 'o', 'COLOR' : libtcod.gold}
    ret['LEGS'] = {'CHAR' : '²', 'COLOR' : libtcod.gray}            # 253
    ret['FEET'] = {'CHAR' : 'ⁿ', 'COLOR' : libtcod.gray}            # 252
    ret['THROWING WEAPON'] = {'CHAR' : '!', 'COLOR' : libtcod.gray}
    return(ret)


