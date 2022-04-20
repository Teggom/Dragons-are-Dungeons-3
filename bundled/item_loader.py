from unit_components.item import Item
from unit_components.damage import Damage
from entity import Entity
from random import sample
import tcod as libtcod
def make_item(name):

    # name, trait, stat, res 
    samp = sample([
        ["", {}, {}, {}],
        [" of Strength", {}, {'strength' : 5}, {'fire_resistance' : 4}],
        [" of Sight", {}, {'sight' : 1}, {'fire_resistance' : 1}],
        [' of Memory', {}, {'memory' : 3}, {'fire_resistance' : 1}],
        [' of Blinding', {}, {'sight' : -3}, {'fire_resistance' : 1}],
        [' of Stupidity', {}, {'memory' : -10}, {'fire_resistance' : -4}],
        [' of Luck', {}, {'luck' : 1}, {'fire_resistance' : 5}],
        [' of Stealth', {"stealth" : 2}, {'dexterity' : 5}, {'fire_resistance' : 1}],
        [' of Godhood', {}, {'strength' : 40, 'dexterity' : 40, 'intelligence' : 40, 'wisdom' : 40, 'charisma' : 100}, {'fire_resistance' : 50}],
        [' of Fire', {}, {}, {'fire_resistance' : 12}]
    ], 1)[0]
    

    if name == 1:
        if samp[0] == ' of Fire':
            dmgs = [Damage("1d6+3", type='slash'), Damage("4", type = "fire")]
        else:
            dmgs = [Damage("1d6+3", type='slash')]
        return(Item(
            "Sword" + samp[0], "Weapon", "/", libtcod.gray, traits = samp[1], stats = samp[2], resistances = samp[3],
            damages=dmgs
        ))
    if name == 2:
        if samp[0] == ' of Fire':
            dmgs = [Damage("2d6+3", type='slash'), Damage("6", type = "fire")]
        else:
            dmgs = [Damage("1d6+3", type='slash')]
        return(Item(
            "Axe" + samp[0], "Weapon", "7", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3],
             damages=dmgs, twohand=True 
        ))
    if name == 3:
        return(Item(
            "Helmet" + samp[0], "Head", "H", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 4:
        return(Item(
            "Chestplate" + samp[0], "Chest", "M", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 5:
        return(Item(
            "Cape" + samp[0], "Back", "4", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 6:
        return(Item(
            "Iron Bracer" + samp[0], "Arm", "z", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 7:
        return(Item(
            "Leather Belt" + samp[0], "Belt", "-", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 8:
        return(Item(
            "Pants" + samp[0], "Legs", "V", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    if name == 9:
        return(Item(
            "Shoe" + samp[0], "Feet", "b", libtcod.gray, traits=samp[1], stats = samp[2], resistances = samp[3]
        ))
    
    if name == 0:
        return(Item(
            "Throwing Axe", "Item", "p", libtcod.silver,
            damages=[Damage("1d4")], quantity=sample([1, 2, 3, 4, 5], 1)[0]
        ))
    pass

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