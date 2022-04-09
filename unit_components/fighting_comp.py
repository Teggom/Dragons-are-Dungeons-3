class stats():
    def __init__(self, unit_type="Human"):
        # Rather than set these below, set them here.
        #  helps keep track of what I have and have not defined
        stat_package = self.get_stat_package(unit_type)

        self.base_hp = stat_package['base_hp']
        self.curr_hp = stat_package['base_hp']
        self.base_mp = stat_package['base_mp']
        self.curr_mp = stat_package['base_mp']
        
        # Core Stats
        self.base_strength = stat_package['base_strength']
        self.base_dexterity = stat_package['base_dexterity']
        self.base_intelligence = stat_package['base_intelligence']
        self.base_charisma = stat_package['base_charisma']
        self.base_wisdom = stat_package['base_wisdom']
        
        # Secondary Stats
        self.base_luck = stat_package['base_luck']
        self.base_memory = stat_package['base_memory']
        self.base_sight = stat_package['base_sight']
        self.base_perception = stat_package['base_perception']
    
    # # # # # #
    # Skills  #
    # # # # # #
    # The following do not take luck or base dice rolls into account
    # Strength
    @property
    def athletics(self):
        Bonus = self.get_skill_mod(self.strength)
        Bonus += self.skill_check_condition("athletics")
        Bonus += self.skill_check_traits("athletics")
        Bonus += self.skill_check_equipment("athletics")
        return(max(0, Bonus))
    
    # Dex
    # Int
    # Wis
    # Cha




    # # # # # # # # #
    # Passive Stats #
    # # # # # # # # #
    @property
    def max_hp(self):
        total = self.base_hp
        total += self.check_condition("max_hp")
        total += self.check_traits("max_hp")
        total += self.check_equipment("max_hp")
        return(max(0, total))

    
    @property
    def hp(self):
        total = self.curr_hp
        total += self.check_condition("hp")
        total += self.check_traits("hp")
        total += self.check_equipment("hp")
        return(max(0, total))

    
    @property
    def max_mp(self):
        total = self.base_mp
        total += self.check_condition("max_mp")
        total += self.check_traits("max_mp")
        total += self.check_equipment("max_mp")
        return(max(0, total))

    
    @property
    def mp(self):
        total = self.curr_mp
        total += self.check_condition("mp")
        total += self.check_traits("mp")
        total += self.check_equipment("mp")
        return(max(0, total))

    # # # # # # # #
    # Core Stats  #
    # # # # # # # #
    @property
    def strength(self):
        total = self.base_strength
        total += self.check_condition("strength")
        total += self.check_traits("strength")
        total += self.check_equipment("strength")
        return(max(0, total))

    
    @property
    def dexterity(self):
        total = self.base_dexterity
        total += self.check_condition("dexterity")
        total += self.check_traits("dexterity")
        total += self.check_equipment("dexterity")
        return(max(0, total))

    
    @property
    def intelligence(self):
        total = self.base_intelligence
        total += self.check_condition("intelligence")
        total += self.check_traits("intelligence")
        total += self.check_equipment("intelligence")
        return(max(0, total))

    
    @property
    def charisma(self):
        total = self.base_charisma
        total += self.check_condition("charisma")
        total += self.check_traits("charisma")
        total += self.check_equipment("charisma")
        return(max(0, total))

    
    @property
    def wisdom(self):
        total = self.base_wisdom
        total += self.check_condition("wisdom")
        total += self.check_traits("wisdom")
        total += self.check_equipment("wisdom")
        return(max(0, total))

    # # # # # # # # # #
    # Secondary Stats #
    # # # # # # # # # #
    
    @property
    def luck(self):
        total = self.base_luck
        total += self.check_condition("luck")
        total += self.check_traits("luck")
        total += self.check_equipment("luck")
        return(max(0, total))

    
    
    @property
    def memory(self):
        run = ""
        total = self.base_memory
        total += self.check_condition("memory")
        total += self.check_traits("memory")
        total += self.check_equipment("memory")
        return(max(0, total))

    @property 
    def sight(self):
        total = self.base_sight
        total += self.check_condition("sight")
        total += self.check_traits("sight")
        total += self.check_equipment("sight")
        return(max(1, total))
    
    # TO MOVE
    @property
    def perception(self):
        total = self.base_perception
        total += self.check_condition("perception")
        total += self.check_traits("perception")
        total += self.check_equipment("perception")
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
                "base_luck" : 3,
                "base_memory" : 8,
                "base_sight" : 6,
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
                "base_luck" : 2,
                "base_memory" : 4,
                "base_sight" : 12,
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
                "base_luck" : 2,
                "base_memory" : 12,
                "base_sight" : 15,
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
                "base_luck" : 1,
                "base_memory" : 4,
                "base_sight" : 4,
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
                "base_luck" : 1,
                "base_memory" : 4,
                "base_sight" : 4,
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
                "base_luck" : 1,
                "base_memory" : 4,
                "base_sight" : 4,
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
                "base_luck" : 1,
                "base_memory" : 1,
                "base_sight" : 1,
                "base_perception" : 1
            })


    # STAT checks
    # Functions for core stats, checks what they are
    # Can exceed 100? Doesn't help
    def check_traits(self, stat):
        total = 0
        for trait in self.owner.traits:
            if trait.modifiers.get(stat):
                total += trait.modifiers.get(stat)
        return(total)

    def check_condition(self, stat):
        total = 0
        for condition in self.owner.conditions:
            if condition.modifiers.get(stat):
                total += condition.modifiers.get(stat)
        return(total)

    def check_equipment(self, stat):
        return(0)




    # SKILL checks
    # Functions for skills, returns the base modifier without luck or d20
    def skill_check_traits(self, skill):
        total = 0
        for trait in self.owner.traits:
            if trait.modifiers.get(skill):
                total += self.skill_level_to_bonus(trait.modifiers.get(skill))
        return(total)

    def skill_check_condition(self, skill):
        total = 0
        for condition in self.owner.conditions:
            if condition.modifiers.get(skill):
                total += self.skill_level_to_bonus(condition.modifiers.get(skill))
        return(total)

    def skill_check_equipment(self, skill):
        return(0)
    




    # Used for converting skill levels and stat values to bonuses for the roll
    #  a ring of acrobatics would have its level used here
    #  ring of acrobatics 3 would have 3 passed in here for a value to use on the dc
    def skill_level_to_bonus(self, skill_level):
        if skill_level <= 0:
            return(0)
        if skill_level == 1:
            return(2)
        if skill_level == 2:
            return(5)
        if skill_level == 3:
            return(9)
        if skill_level == 4:
            return(14)
        if skill_level >= 5:
            return(20)


    # Skill mod. here, 50 strength gives 8 to roll 
    def get_skill_mod(self, stat_value):
        if stat_value <= 1:
            return(-5)
        if stat_value <= 2:
            return(-4)
        if stat_value <= 3:
            return(-3)
        if stat_value <= 5:
            return(-2)
        if stat_value <= 7:
            return(-1)
        if stat_value <= 10:
            return(0)
        if stat_value <= 13:
            return(1)
        if stat_value <= 17:
            return(2)
        if stat_value <= 21:
            return(3)
        if stat_value <= 26:
            return(4)
        if stat_value <= 31:
            return(5)
        if stat_value <= 37:
            return(6)
        if stat_value <= 43:
            return(7)
        if stat_value <= 56:
            return(8)
        if stat_value <= 64:
            return(9)
        if stat_value <= 73:
            return(10)
        if stat_value <= 82:
            return(11)
        if stat_value <= 91:
            return(12)
        if stat_value <= 100:
            return(13)
        if stat_value > 100:
            return(15)
                    