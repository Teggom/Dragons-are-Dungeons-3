class resistance_comp():
    def __init__(self, *args, **kwargs):
        self.stat_denom = 20
        res_names = [
            'fire_resistance',
            'frost_resistance',
            'shock_resistance',
            'arcane_resistance', 
            'poison_resistance',
            'holy_resistance',
            'unholy_resistance',
            'pure_resistance',
            'blunt_resistance',
            'slash_resistance',
            'pierce_resistance'
        ]
        self.resistances = {}
        for res in res_names:
            if res in kwargs:
                self.resistances["base_" + res] = kwargs[res]
            else:
                self.resistances["base_" + res] = 0
    

    def get_this_item_resistance(self, res):
        total = self.resistances["base_" + res + "_resistance"]
        if self.owner.traits.on_item['resistances'].get(res):
                total += self.owner.traits.on_item['resistances'].get(res)
        return(total)


    # pass the stat as a single string
    def get_resistance(self, res, percent = True, get = ['base', 'equip', 'traits', 'conditions']):
        total = 0
        if 'base' in get:
            total += self.resistances["base_" + res + "_resistance"]
        if 'equip' in get:
            total += self.res_check_equipment(res + "_resistance")
        if 'trait' in get:
            total += self.res_check_trait(res + "_resistance")
        if 'conditions' in get:
            total += self.res_check_condition(res + "_resistance")
        if percent:
            if total < 0:
                extra = abs(total)/(self.stat_denom+abs(total))
            else:
                extra = 0
            
            damage_percent = 1 - total / (total + self.stat_denom) + extra**1.2
            
            return(damage_percent)
        else:
            return(total)

    # Equipment has X_resistance
    def res_check_equipment(self, resistance):
        total = 0
        if self.owner.inventory:
            for gear_slot in self.owner.inventory.wearing.keys():
                if self.owner.inventory.wearing[gear_slot]:
                    if self.owner.inventory.wearing[gear_slot].resistances.get(resistance):
                        total += self.owner.inventory.wearing[gear_slot].resistances.get(resistance)
                    if self.owner.inventory.wearing[gear_slot].trait:
                        if self.owner.inventory.wearing[gear_slot].trait.on_item['resistances'].get(resistance):
                            total += self.owner.inventory.wearing[gear_slot].trait.on_item['resistances'].get(resistance)
                    if len(self.owner.inventory.wearing[gear_slot].conditions) > 0:
                        for cond in self.owner.inventory.wearing[gear_slot].conditions:
                            if cond.on_item['resistances'].get(resistance):
                                total += cond.on_item['resistances'].get(resistance)
        return(total)
    
    def res_check_condition(self, resistance):
        total = 0
        if self.owner.conditions:
            for condition in self.owner.conditions:
                if condition.on_char['resistances'].get(resistance):
                    total += condition.on_char['resistances'].get(resistance)
        return(total)

    def res_check_trait(self, resistance):
        total = 0
        if self.owner.traits:
            for trait in self.owner.traits:
                if trait.on_char['resistances'].get(resistance):
                    total += trait.on_char['resistances'].get(resistance)
        return(total)