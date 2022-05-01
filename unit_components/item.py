# Damage is of the form
# {"dice_rolls" : <int>, "upper" : <int>, "flat" : <int>}
# an axe doing 2d6+3 would be
#   {"dice_rolls" : 2, "upper" : 6, "flat" : 3}
#   sum(random.sample(range(upper), dice_rolls))+dice_rolls+flat
# Resistance is applied to items and traits as "X_resistance"
class Item:
    def __init__(
            self, 
            name, 
            type, 
            vis_package, 
            x=None, y=None, 
            noise =             0,
            trait =             None, 
            conditions =        [], # list of traits
            stats =             {}, # key-val of stats
            skills =            {}, # key-val of skills
            resistances =       {}, # key-val of resistances
            damages =           [], # list of damages if this is a weapon
            twohand =           False, # is this a two hand weapon
            perturn_func =      [], # Functions that activate every turn this is worn / on the ground?
            peruse_func  =      [], # Functions that activate when this item is used
            onhit_enemy_func =  [], # Functions that activate when this item is used on a character or thing
            quantity =          1   # quantity of this item
            ):
        self.name = name
        self.type = type
        self.vis_package = vis_package
        self.char = self.vis_package['CHAR']
        self.color = self.vis_package['COLOR']
        self.x = x
        self.y = y
        self.noise = noise
        self.trait = trait
        self.conditions = conditions
        self.stats = stats
        self.skills = skills
        self.resistances = resistances
        self.damages = damages
        self.twohand = twohand
        self.perturn_func = perturn_func,
        self.peruse_func = peruse_func,
        self.onhit_enemy_func = onhit_enemy_func,
        self.quantity = quantity
        
    @property
    def q_name(self):
        if self.trait:
            if self.trait.item_namechange[0] == 0:
                nname = self.trait.item_namechange[1] + " " + self.name
            else:
                nname = self.name + " " + self.trait.item_namechange[1]
        else:
            nname = self.name
        if self.quantity > 1:
            return(str(nname) + " x" + str(self.quantity))
        else:
            return(str(nname))
    
    @property
    def t_name(self):
        if self.trait:
            if self.trait.item_namechange[0] == 0:
                nname = self.trait.item_namechange[1] + " " + self.name
            else:
                nname = self.name + " " + self.trait.item_namechange[1]
        else:
            return(self.name)
        return(nname)


    def copy_self(self, quantity = 1):
        n_item = Item(
            name = self.name, 
            type=self.type, 
            vis_package=self.vis_package, 
            x=self.x, y=self.y, 
            trait=self.trait, 
            conditions = self.conditions,
            stats = self.stats, 
            skills = self.skills,
            resistances = self.resistances, 
            damages=self.damages,
            twohand = self.twohand, 
            perturn_func = self.perturn_func,
            peruse_func= self.peruse_func,
            onhit_enemy_func=self.onhit_enemy_func,            
            quantity=quantity)
        n_item.owner = self.owner
        return(n_item)
    
    def get_damage(self):
        damage = 0
        for dmg_obj in self.damages:
            damage += dmg_obj.get_damage()
        return(max(0, damage))
    
    def __str__(self):
        if self.trait:
            if self.trait.item_namechange[0] == 0:
                nname = self.trait.item_namechange[1] + " " + self.name
            else:
                nname = self.name + " " + self.trait.item_namechange[1]
        else:
            nname = self.name
        if self.quantity > 1:
            return(str(nname) + " x" + str(self.quantity))
        else:
            return(str(nname))