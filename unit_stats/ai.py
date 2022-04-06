import tcod as libtcod
from random import sample
class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.stats.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))

class BasicMerchant:
    def take_turn(self, target, fov_map, game_map, entities):
        merchant = self.owner
        if libtcod.map_is_in_fov(fov_map, merchant.x, merchant.y):

            if merchant.distance_to(target) >= 2:
                merchant.move_towards(target.x, target.y, game_map, entities)

            elif target.stats.hp > 0:
                print('The {0} asks, "My Potions are to strong for you traveler!"'.format(merchant.name))

class Wander:
    def take_turn(self, target, fov_map, game_map, entities):
        loser = self.owner
        # Could have jsut sampled a double list huh...
        dx, dy = {1:(-1, 0),2:(1, 0),3:(0, 1),4:(0,-1)}[sample([1, 2, 3, 4], 1)[0]]
        if not game_map.tiles[loser.x+dx][loser.y+dy].blocked:
            loser.move(dx, dy)
        else:
            print('The filthy {0} screams and smashes their head on the cave wall.'.format(loser.name))