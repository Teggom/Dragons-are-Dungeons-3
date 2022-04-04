class stats():
    def __init__(self, owner, unit_type="Human"):
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
        self.owner = owner
    
    @property
    def max_hp(self):
        return(self.base_hp)
    
    @property
    def hp(self):
        return(self.curr_hp)
    
    @property
    def strength(self):
        return(self.base_strength)
    
    @property
    def dexterity(self):
        return(self.base_dexterity)
    
    @property
    def intelligence(self):
        return(self.base_intelligence)
    
    @property
    def charisma(self):
        return(self.base_charisma)
    
    @property
    def wisdom(self):
        return(self.base_wisdom)
    
    @property
    def endurance(self):
        return(self.base_endurance)
    
    @property
    def luck(self):
        return(self.base_luck)
    
    def get_stat_package(self, unit_type):
        if unit_type == "Human":
            tup = (20, 10, 8, 6, 6, 5, 5, 7, 3)
        elif unit_type == "Elf":
            tup = (15, 20, 5, 8, 8, 9, 8, 3, 2)
        elif unit_type == "Dwarf":
            tup = (30, 5, 11, 8, 6, 4, 6, 10, 2)
        elif unit_type == "Goblin":
            tup = (12, 2, 6, 4, 2, 1, 2, 4, 1)
        else:
            # No type found
            tup = (1, 1, 1, 1, 1, 1, 1, 1, 1)
        package = tup
        return({
            "base_hp" : package[0],
            "base_mp" : package[1],
            "base_strength" : package[2],
            "base_dexterity" : package[3],
            "base_intelligence" : package[4],
            "base_charisma" : package[5],
            "base_wisdom" : package[6],
            "base_endurance" : package[7],
            "base_luck" : package[8]
        })