from bundled.game_messages import Message
from unit_components.fighting_comp import stats
from unit_components.ai import Wander, BasicMerchant, BasicMonster
from unit_components.inventory import Inventory
import math
import tcod as libtcod

from unit_components.resistances import resistance_comp


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, race=None, clss = None, blocks=False, ai=None, traits=[],
                    item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.race = race
        self.clss = clss
        self.blocks = blocks
        self.stats = stats(race)
        self.stats.owner = self 
        self.stats.resistances.owner = self
        self.ai = ai
        self.dead = False
        self.traits = traits
        self.conditions = []
        self.item = item
        self.inventory = inventory

        if not self.inventory:
            self.inventory = Inventory()

        if self.ai:
            self.ai.owner = self
        
        if self.item:
            self.item.owner = self
        
        if self.inventory:
            self.inventory.owner = self

        
        self.stats.curr_hp = self.stats.max_hp
        self.stats.curr_mp = self.stats.max_mp


    @property
    def diff(self):
        diff = 0
        for trait in self.traits:
            for skill in trait.on_char['skills']:
                diff += trait.on_char['skills'][skill]
            for stat in trait.on_char['stats']:
                diff += trait.on_char['stats'][stat]
            for res in trait.on_char['resistances']:
                diff += trait.on_char['resistances'][res]
            diff += len(trait.on_char['perturn_func'])*3
        
        for condition in self.conditions:
            for skill in condition.on_char['skills']:
                diff += condition.on_char['skills'][skill]
            for stat in condition.on_char['stats']:
                diff += condition.on_char['stats'][stat]
            for res in condition.on_char['resistances']:
                diff += condition.on_char['resistances'][res]
            diff += len(condition.on_char['perturn_func'])*3
        
        for gear_slot in self.inventory.wearing.keys():
            if self.inventory.wearing[gear_slot]:
                diff += int(1 + self.inventory.wearing[gear_slot].value / 20 )
        # stats
        diff += self.stats.luck*5
        diff += self.stats.sight*2
        diff += self.stats.perception
        diff += self.stats.max_hp
        diff += self.stats.max_mp
        diff += self.stats.strength
        diff += self.stats.dexterity
        diff += self.stats.intelligence
        diff += self.stats.wisdom
        diff += self.stats.charisma

        return(diff)

        # skills
        # resistances

    def give_condition(self, condition):
        self.conditions.append(condition)

    def kill(self):
        self.dead = True
        self.color = libtcod.Color(100, 0, 0)

    def step(self):
        # happens each turn, idle things like countdowns or cooldowns
        for condition in self.conditions:
            if condition.duration < 1:
                print("Condition {} affecting {} has gone away.".format(condition.name, self.name))
                self.conditions.remove(condition)
            else:
                condition.duration -= 1

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
    
    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)    
    
    # Where damage is a list of damage items
    def take_damage(self, damage):
        damage_to_take = {}
        for dmg in damage:
            if dmg.type in damage_to_take:
                damage_to_take[dmg.type] += dmg.get_damage()[0]
            else:
                damage_to_take[dmg.type] = dmg.get_damage()[0]
        taking = 0
        for d_type in damage_to_take.keys():
            taking += math.ceil(
                damage_to_take[d_type] * self.stats.resistances.get_resistance(d_type)
            )
        self.stats.curr_hp = max(0, self.stats.curr_hp - taking)
        return(Message("{} takes {} damage!".format(self.name, taking), color = libtcod.darker_red))

        
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
