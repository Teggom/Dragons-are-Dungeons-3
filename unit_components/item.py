# Damage is of the form
# {"dice_rolls" : <int>, "upper" : <int>, "flat" : <int>}
# an axe doing 2d6+3 would be
#   {"dice_rolls" : 2, "upper" : 6, "flat" : 3}
#   sum(random.sample(range(upper), dice_rolls))+dice_rolls+flat
# Resistance is applied to items and traits as "X_resistance"
import random


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
            subtype =           None,
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
        self.perturn_func = perturn_func
        self.peruse_func = peruse_func
        self.onhit_enemy_func = onhit_enemy_func
        self.quantity = quantity

        if not subtype:
            self.subtype = self.type
        else:
            self.subtype = subtype
        
    def dist_to_entity(self, other_entity):
        return(
            ((self.x-other_entity.x)**2 + (self.y-other_entity.y)**2)**(1/2)
        )

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

    @property
    def value(self):
        return(int(self.s_value))

    @property
    def s_value(self):
        value = 0
        
        if self.perturn_func is not None:
            value += len(self.perturn_func)*10
        value += len(self.peruse_func)*10
        value += len(self.onhit_enemy_func)*20

        for dmg in self.damages:
            value += dmg.avg

        for key in self.resistances.keys():
            if self.resistances[key] > 0:
                value += self.resistances[key]
            else:
                # negative is punished more
                value += self.resistances[key]*2

        for key in self.skills.keys():
            value += self.skills[key]*4
        
        for key in self.stats.keys():
            value += self.stats[key]
        
        if self.trait:
            value += 15
            for key in self.trait.on_item['skills'].keys():
                value += self.trait.on_item['skills'][key]*4
            for key in self.trait.on_item['stats'].keys():
                value += self.trait.on_item['stats'][key]
            for key in self.trait.on_item['resistances'].keys():
                if self.trait.on_item['resistances'][key] > 0:
                    value += self.trait.on_item['resistances'][key]
                else:
                    value += self.trait.on_item['resistances'][key]*2
            for dmg in self.trait.on_item['onhit_damage']:
                value += dmg.avg
            value += len(self.trait.on_item['perturn_func'])*10
            value += len(self.trait.on_item['onhit_enemy_func'])*20
        
        bonus_1 = ord(self.name[0])*0.0001
        bonus_2 = ord(self.name[1])*0.0000001
        bonus_3 = ord(self.name[len(self.name)-1])*0.0000000001
        bonus_4 = ord(self.name[len(self.name)-2])*0.0000000000001
        return(value + bonus_1 + bonus_2 + bonus_3 + bonus_4)
    
    # def print_value(self):
    #     value = 0
        
    #     if self.perturn_func is not None:
    #         value += len(self.perturn_func)*10
    #     print(value, 1, len(self.perturn_func), self.perturn_func)
    #     value += len(self.peruse_func)*10
    #     print(value, 2)
    #     value += len(self.onhit_enemy_func)*20
    #     print(value, 3)

    #     for dmg in self.damages:
    #         value += dmg.avg
    #     print(value, 4)

    #     for key in self.resistances.keys():
    #         if self.resistances[key] > 0:
    #             value += self.resistances[key]
    #         else:
    #             # negative is punished more
    #             value += self.resistances[key]*2

    #     print(value, 5)

    #     for key in self.skills.keys():
    #         value += self.skills[key]*4
        
    #     print(value, 6)
    #     for key in self.stats.keys():
    #         value += self.stats[key]
        
    #     print(value, 7)
    #     if self.trait:
    #         value += 15
    #         for key in self.trait.on_item['skills'].keys():
    #             value += self.trait.on_item['skills'][key]*4
    #         for key in self.trait.on_item['stats'].keys():
    #             value += self.trait.on_item['stats'][key]
    #         for key in self.trait.on_item['resistances'].keys():
    #             if self.trait.on_item['resistances'][key] > 0:
    #                 value += self.trait.on_item['resistances'][key]
    #             else:
    #                 value += self.trait.on_item['resistances'][key]*2
    #         for dmg in self.trait.on_item['onhit_damage']:
    #             value += dmg.avg
    #         value += len(self.trait.on_item['perturn_func'])*10
    #         value += len(self.trait.on_item['onhit_enemy_func'])*20
    #     return(int(value))

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
            subtype=self.subtype,        
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