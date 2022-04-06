from map_objects.tile import Tile
class animation:
    def __init__(self, x0, y0, x1, y1, type, affect_walls=False, block_sight = False, duration = 10):
        self.current_step = 0
        self.duration = duration
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.type = type
        self.affect_walls = affect_walls
        self.block_sight = block_sight
        self.finished = False


    # gets current effects and returns next set of tiles to draw
    def next_step(self):
        self.current_step+=1
        if self.current_step==self.duration:
            self.finished = True
        if self.type == 'burn':
            return(Tile(False, "Burn", self.x0, self.y0))
