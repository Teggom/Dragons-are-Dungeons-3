# Damage is of the form
# {"dice_rolls" : <int>, "upper" : <int>, "flat" : <int>}
# an axe doing 2d6+3 would be
#   {"dice_rolls" : 2, "upper" : 6, "flat" : 3}
#   sum(random.sample(range(upper), dice_rolls))+dice_rolls+flat
class Item:
    def __init__(self, name, type, char, color, x=None, y=None, traits = {}, stats = {}, damages = [], twohand = False, quantity = 1):
        self.name = name
        self.type = type
        self.char = char
        self.color = color
        self.x = x
        self.y = y
        self.traits = traits
        self.stats = stats
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
        n_item = Item(self.name, self.type, self.char, self.color, self.x, self.y, self.traits, self.stats, self.damages, self.twohand, quantity=quantity)
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