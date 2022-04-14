from unit_components.item import Item
from unit_components.damage import Damage
from entity import Entity
from random import sample
import tcod as libtcod
def make_item(name):
    additional_name = sample([' of Fire', '', ' of Ice', 
        " of Sight", ' of Blinding', ' of Strength'], 1)[0]
    if name == "Sword":
        return(Item(
            "Sword" + additional_name, "Weapon", "/", libtcod.gray,
            damages=[Damage("1d6+3")]
        ))
    if name == "Amulet":
        return(Item(
            "Amulet" + additional_name, "Neck", "o", libtcod.white,
            traits={"Memory" : 5}
        ))
    if name == "Glove":
        return(Item(
            "Leather Glove" + additional_name, "Arm", "m", libtcod.Color(165, 103, 69),
        ))
    if name == "Item":
        return(Item(
            "Throwing Axe", "Item", "p", libtcod.silver,
            damages=[Damage("1d4")]
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