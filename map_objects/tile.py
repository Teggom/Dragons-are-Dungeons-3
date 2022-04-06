from random import random, sample
import tcod as libtcod
class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, palette_type, x, y, state = 0, block_sight=None, palette_seed = None):
        self.x = x
        self.y = y
        self.state = state
        self.blocked = blocked
        self.set_palette(palette_type, palette_seed)
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False
        self.last_seen = 0

    def step(self, player):
        self.last_seen += 1
        if self.last_seen / (4**player.stats.memory + self.last_seen) > random():
            self.explored = False
            self.last_seen = 0
            return(True)
        return(False)
    
    def update_tile(self, blocked, palette_type, x, y, state = 0, block_sight=None, palette_seed=None):
        self.x = x
        self.y = y
        self.state = state
        self.blocked = blocked
        self.set_palette(palette_type, palette_seed)
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = self.explored
        self.last_seen = self.last_seen

    def get_color(self, state):
        if not state in self.palette.keys():
            return(libtcod.Color(255, 255, 255))
        else:
            return(self.palette[state])

    def set_palette(self, palette_type, palette_seed):
        if self.blocked:
            VAL_1 = 5
        else:
            VAL_1 = 12
        palette_seed_spread = [
            (0,         0,          0),
            (0,         VAL_1,      0),
            (VAL_1,     0,          0),
            (0,         0,          VAL_1),
            (VAL_1,     VAL_1,      0),
            (VAL_1,     0,          VAL_1),
            (VAL_1,     VAL_1,      0),
            (VAL_1,     VAL_1,      VAL_1)
        ]
        if palette_seed and palette_seed < len(palette_seed_spread):
            palette_mod = palette_seed_spread[palette_seed]
        else:
            palette_mod = palette_seed_spread[sample(range(len(palette_seed_spread)), 1)[0]]
        palettes = {
            "Wall" : {
                "Unseen" : libtcod.Color(0, 0, 0),
                "Visible" : libtcod.Color(130, 110, 50),
                "Explored" : libtcod.Color(0, 0, 100)
            },
            "Floor" : {
                "Unseen" : libtcod.Color(0, 0, 0),
                "Visible" : libtcod.Color(200, 180, 50),
                "Explored" : libtcod.Color(50, 50, 150)
            }
            # "Burn" : {
            #     "Unseen" : libtcod.Color(0,0,0),
            #     "Visible" : libtcod.Color(230-self.state*13, 0+self.state*10, 0+self.state*10),
            #     "Explored" : libtcod.Color(0,0,0)
            # }

        }
        picked = palettes[palette_type]
        for key in picked.keys():
            picked[key] -= palette_mod
        self.palette = picked
        
