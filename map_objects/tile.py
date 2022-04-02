from random import random
import tcod as libtcod
class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, pallet_type, block_sight=None):
        self.blocked = blocked
        self.pallet = self.get_pallet(pallet_type)
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False
        self.last_seen = 0

    def step(self):
        self.last_seen += 1
        if self.last_seen / (1000 + self.last_seen) > random():
            self.explored = False
            self.last_seen = 0
            return(True)
        return(False)
    
    def update_tile(self, blocked, pallet_type, block_sight=None):
        self.blocked = blocked
        self.pallet = self.get_pallet(pallet_type)
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = self.explored
        self.last_seen = self.last_seen

    def get_pallet(self, pallet_type):
        pallets = {
            "Wall" : {
                "Unseen" : libtcod.Color(0, 0, 0),
                "Visible" : libtcod.Color(130, 110, 50),
                "Explored" : libtcod.Color(0, 0, 100),
            },
            "Floor" : {
                "Unseen" : libtcod.Color(0, 0, 0),
                "Visible" : libtcod.Color(200, 180, 50),
                "Explored" : libtcod.Color(50, 50, 150),
            }
        }
        
