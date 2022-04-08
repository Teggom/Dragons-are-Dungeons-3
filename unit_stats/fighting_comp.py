class stats():
    def __init__(self, unit_type="Human"):
        # Rather than set these below, set them here.
        #  helps keep track of what I have and have not defined
        stat_package = self.get_stat_package(unit_type)
        self.base_hp = stat_package['base_hp']
        self.curr_hp = stat_package['base_hp']
        self.base_mp = stat_package['base_mp']
        self.curr_mp = stat_package['base_mp']
        self.base_strength = stat_package['base_strength']
        self.base_dexterity = stat_package['base_dexterity']
        self.base_intelligence = stat_package['base_intelligence']
        self.base_charisma = stat_package['base_charisma']
        self.base_wisdom = stat_package['base_wisdom']
        self.base_endurance = stat_package['base_endurance']
        self.base_luck = stat_package['base_luck']
        self.base_memory = stat_package['base_memory']
        self.base_fov = stat_package['base_fov']
        self.base_perception = stat_package['base_perception']
    

    @property
    def max_hp(self):
        total = self.base_hp
        for trait in self.owner.traits:
            if trait.modifiers.get('max_hp'):
                total += trait.modifiers.get('max_hp')
        for condition in self.owner.conditions:
            if condition.modifiers.get('max_hp'):
                total += condition.modifiers.get('max_hp')
        return(max(0, total))
    
    @property
    def hp(self):
        total = self.curr_hp
        for trait in self.owner.traits:
            if trait.modifiers.get('curr_hp'):
                total += trait.modifiers.get('curr_hp')
        for condition in self.owner.conditions:
            if condition.modifiers.get('curr_hp'):
                total += condition.modifiers.get('curr_hp')
        return(max(0, total))
    
    @property
    def max_mp(self):
        total = self.base_mp
        for trait in self.owner.traits:
            if trait.modifiers.get('max_mp'):
                total += trait.modifiers.get('max_mp')
        for condition in self.owner.conditions:
            if condition.modifiers.get('max_mp'):
                total += condition.modifiers.get('max_mp')
        return(max(0, total))
    
    @property
    def mp(self):
        total = self.curr_mp
        for trait in self.owner.traits:
            if trait.modifiers.get('curr_mp'):
                total += trait.modifiers.get('curr_mp')
        for condition in self.owner.conditions:
            if condition.modifiers.get('curr_mp'):
                total += condition.modifiers.get('curr_mp')
        return(max(0, total))

    @property
    def strength(self):
        total = self.base_strength
        for trait in self.owner.traits:
            if trait.modifiers.get('strength'):
                total += trait.modifiers.get('strength')
        for condition in self.owner.conditions:
            if condition.modifiers.get('strength'):
                total += condition.modifiers.get('strength')
        return(max(0, total))
    
    @property
    def dexterity(self):
        total = self.base_dexterity
        for trait in self.owner.traits:
            if trait.modifiers.get('dexterity'):
                total += trait.modifiers.get('dexterity')
        for condition in self.owner.conditions:
            if condition.modifiers.get('dexterity'):
                total += condition.modifiers.get('dexterity')
        return(max(0, total))
    
    @property
    def intelligence(self):
        total = self.base_intelligence
        for trait in self.owner.traits:
            if trait.modifiers.get('intelligence'):
                total += trait.modifiers.get('intelligence')
        for condition in self.owner.conditions:
            if condition.modifiers.get('intelligence'):
                total += condition.modifiers.get('intelligence')
        return(max(0, total))
    
    @property
    def charisma(self):
        total = self.base_charisma
        for trait in self.owner.traits:
            if trait.modifiers.get('charisma'):
                total += trait.modifiers.get('charisma')
        for condition in self.owner.conditions:
            if condition.modifiers.get('charisma'):
                total += condition.modifiers.get('charisma')
        return(max(0, total))
    
    @property
    def wisdom(self):
        total = self.base_wisdom
        for trait in self.owner.traits:
            if trait.modifiers.get('wisdom'):
                total += trait.modifiers.get('wisdom')
        for condition in self.owner.conditions:
            if condition.modifiers.get('wisdom'):
                total += condition.modifiers.get('wisdom')
        return(max(0, total))
    
    @property
    def endurance(self):
        total = self.base_endurance
        for trait in self.owner.traits:
            if trait.modifiers.get('endurance'):
                total += trait.modifiers.get('endurance')
        for condition in self.owner.conditions:
            if condition.modifiers.get('endurance'):
                total += condition.modifiers.get('endurance')
        return(max(0, total))
    
    @property
    def luck(self):
        total = self.base_luck
        for trait in self.owner.traits:
            if trait.modifiers.get('luck'):
                total += trait.modifiers.get('luck')
        for condition in self.owner.conditions:
            if condition.modifiers.get('luck'):
                total += condition.modifiers.get('luck')
        return(max(0, total))
    
    
    @property
    def memory(self):
        total = self.base_memory
        for trait in self.owner.traits:
            if trait.modifiers.get('memory'):
                total += trait.modifiers.get('memory')
        for condition in self.owner.conditions:
            if condition.modifiers.get('memory'):
                total += condition.modifiers.get('memory')
        return(max(0, total))

    @property 
    def fov(self):
        total = self.base_fov
        for trait in self.owner.traits:
            if trait.modifiers.get('fov'):
                total += trait.modifiers.get('fov')
        for condition in self.owner.conditions:
            if condition.modifiers.get('fov'):
                total += condition.modifiers.get('fov')
        return(max(1, total))
    
    @property
    def perception(self):
        total = self.base_perception
        for trait in self.owner.traits:
            if trait.modifiers.get('perception'):
                total += trait.modifiers.get('perception')
        for condition in self.owner.conditions:
            if condition.modifiers.get('perception'):
                total += condition.modifiers.get('perception')
        return(max(0, total))

    def get_stat_package(self, unit_type):
        if unit_type == "Human":
            return({
                "base_hp" : 20,
                "base_mp" : 10,
                "base_strength" : 8,
                "base_dexterity" : 6,
                "base_intelligence" : 6,
                "base_charisma" : 5,
                "base_wisdom" : 5,
                "base_endurance" : 7,
                "base_luck" : 3,
                "base_memory" : 8,
                "base_fov" : 6,
                "base_perception" : 6
            })
        elif unit_type == "Elf":
            return({
                "base_hp" : 15,
                "base_mp" : 20,
                "base_strength" : 5,
                "base_dexterity" : 8,
                "base_intelligence" : 8,
                "base_charisma" : 9,
                "base_wisdom" : 8,
                "base_endurance" : 3,
                "base_luck" : 2,
                "base_memory" : 4,
                "base_fov" : 12,
                "base_perception" : 7
            })
        elif unit_type == "Dwarf":
            return({
                "base_hp" : 30,
                "base_mp" : 5,
                "base_strength" : 11,
                "base_dexterity" : 8,
                "base_intelligence" : 6,
                "base_charisma" : 4,
                "base_wisdom" : 6,
                "base_endurance" : 10,
                "base_luck" : 2,
                "base_memory" : 12,
                "base_fov" : 15,
                "base_perception" : 6
            })
        elif unit_type == "Goblin":
            return({
                "base_hp" : 12,
                "base_mp" : 2,
                "base_strength" : 6,
                "base_dexterity" : 4,
                "base_intelligence" : 2,
                "base_charisma" : 1,
                "base_wisdom" : 2,
                "base_endurance" : 4,
                "base_luck" : 1,
                "base_memory" : 4,
                "base_fov" : 4,
                "base_perception" : 3
            })
        elif unit_type == "Orc":
            return({
                "base_hp" : 20,
                "base_mp" : 0,
                "base_strength" : 8,
                "base_dexterity" : 4,
                "base_intelligence" : 2,
                "base_charisma" : 1,
                "base_wisdom" : 2,
                "base_endurance" : 4,
                "base_luck" : 1,
                "base_memory" : 4,
                "base_fov" : 4,
                "base_perception" : 2
            })
        elif unit_type == "Troll":
            return({
                "base_hp" : 40,
                "base_mp" : 0,
                "base_strength" : 12,
                "base_dexterity" : 4,
                "base_intelligence" : 2,
                "base_charisma" : 1,
                "base_wisdom" : 2,
                "base_endurance" : 4,
                "base_luck" : 1,
                "base_memory" : 4,
                "base_fov" : 4,
                "base_perception" : 3
            })
        else:
            # No type found
            return({
                "base_hp" : 1,
                "base_mp" : 1,
                "base_strength" : 1,
                "base_dexterity" : 1,
                "base_intelligence" : 1,
                "base_charisma" : 1,
                "base_wisdom" : 1,
                "base_endurance" : 1,
                "base_luck" : 1,
                "base_memory" : 1,
                "base_fov" : 1,
                "base_perception" : 1
            })
            