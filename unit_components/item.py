# Damage is of the form
# {"dice_rolls" : <int>, "upper" : <int>, "flat" : <int>}
# an axe doing 2d6+3 would be
#   {"dice_rolls" : 2, "upper" : 6, "flat" : 3}
#   sum(random.sample(range(upper), dice_rolls))+dice_rolls+flat
# Resistance is applied to items and traits as "X_resistance"
class Item:
    def __init__(self, name, type, vis_package, x=None, y=None, traits = {}, stats = {}, resistances = {}, damages = [], twohand = False, quantity = 1):
        self.name = name
        self.type = type
        self.vis_package = vis_package
        self.char = self.vis_package['CHAR']
        self.color = self.vis_package['COLOR']
        self.x = x
        self.y = y
        self.traits = traits
        self.stats = stats
        self.resistances = resistances
        self.damages = damages
        self.twohand = twohand
        self.quantity = quantity
        
    @property
    def q_name(self):
        if self.quantity <= 1:
            return(self.name)
        else:
            return(self.name + " x" + str(self.quantity))

    def copy_self(self, quantity = 1):
        n_item = Item(name = self.name, type=self.type, vis_package=self.vis_package, x=self.x, y=self.y, traits=self.traits, 
            stats = self.stats, resistances = self.resistances, damages=self.damages,
            twohand = self.twohand, quantity=quantity)
        n_item.owner = self.owner
        return(n_item)
    
    def get_damage(self):
        damage = 0
        for dmg_obj in self.damages:
            damage += dmg_obj.get_damage()
        return(max(0, damage))
    
    def __str__(self):
        if self.quantity > 1:
            return(str(self.name) + " x" + str(self.quantity))
        else:
            return(str(self.name))