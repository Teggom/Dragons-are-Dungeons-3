from unit_components.leveling import level_tracker
from unit_components.resistances import resistance_comp


class stats():
    def __init__(self, unit_type="Human", level_comp = level_tracker(), resistances = resistance_comp()):
        # Rather than set these below, set them here.
        #  helps keep track of what I have and have not defined
        stat_package = self.get_stat_package(unit_type)
        self.resistances = resistances

        # self.base_hp = stat_package['base_hp']
        # self.curr_hp = stat_package['base_hp']
        # self.base_mp = stat_package['base_mp']
        # self.curr_mp = stat_package['base_mp']
        
        # Core Stats
        
        # self.base_strength = stat_package['base_strength']
        # self.base_dexterity = stat_package['base_dexterity']
        # self.base_intelligence = stat_package['base_intelligence']
        # self.base_charisma = stat_package['base_charisma']
        # self.base_wisdom = stat_package['base_wisdom']
        
        # Secondary Stats
        self.base_luck = stat_package['base_luck']
        self.base_memory = stat_package['base_memory']
        self.base_sight = stat_package['base_sight']
        self.base_perception = stat_package['base_perception']

        # TODO CHANGE THIS, it's overriding the parameters passed in
        self.level_tracker = level_tracker(
            strength = stat_package['base_strength'],
            dexterity = stat_package['base_dexterity'],
            intelligence = stat_package['base_intelligence'],
            wisdom = stat_package['base_wisdom'],
            charisma = stat_package['base_charisma'],
            base_hp = stat_package['base_hp'],
            base_mp = stat_package['base_mp']
        )
        self.level_tracker.owner = self
        self.curr_hp = self.base_hp
        self.curr_mp = self.base_mp
        
    
    # # # # # #
    # Skills  #
    # # # # # #
    # The following do not take luck or base dice rolls into account
    # Strength
    @property
    def athletics(self):
        Bonus = self.get_skill_mod(self.strength)
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['athletics']['level'])
        Bonus += self.skill_check_condition("athletics")
        Bonus += self.skill_check_traits("athletics")
        Bonus += self.skill_check_equipment("athletics")
        return(Bonus)
        #return(max(0, Bonus))

    
    @property
    def acrobatics(self):
        Bonus = self.get_skill_mod(int(self.dexterity*.5) + int(self.strength*.5))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['acrobatics']['level'])
        Bonus += self.skill_check_condition("acrobatics")
        Bonus += self.skill_check_traits("acrobatics")
        Bonus += self.skill_check_equipment("acrobatics")
        return(Bonus)
        #return(max(0, Bonus))


    # Dex
    @property
    def slight_of_hand(self):
        Bonus = self.get_skill_mod(self.dexterity)
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['slight_of_hand']['level'])
        Bonus += self.skill_check_condition("slight_of_hand")
        Bonus += self.skill_check_traits("slight_of_hand")
        Bonus += self.skill_check_equipment("slight_of_hand")
        return(Bonus)
        #return(max(0, Bonus))


    @property
    def stealth(self):
        Bonus = self.get_skill_mod(int(self.dexterity*.75) + int(self.wisdom*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['stealth']['level'])
        Bonus += self.skill_check_condition("stealth")
        Bonus += self.skill_check_traits("stealth")
        Bonus += self.skill_check_equipment("stealth")
        return(Bonus)
        #return(max(0, Bonus))

    
    # Int
    @property
    def arcana(self):
        Bonus = self.get_skill_mod(self.intelligence)
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['arcana']['level'])
        Bonus += self.skill_check_condition("arcana")
        Bonus += self.skill_check_traits("arcana")
        Bonus += self.skill_check_equipment("arcana")
        return(Bonus)
        #return(max(0, Bonus))

    
    @property
    def alchemy(self):
        Bonus = self.get_skill_mod(int(self.intelligence*.75) + int(self.wisdom*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['alchemy']['level'])
        Bonus += self.skill_check_condition("alchemy")
        Bonus += self.skill_check_traits("alchemy")
        Bonus += self.skill_check_equipment("alchemy")
        return(Bonus)
        #return(max(0, Bonus))

    
    # Wis
    @property
    def crafting(self):
        Bonus = self.get_skill_mod(int(self.wisdom*.75) + int(self.dexterity*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['crafting']['level'])
        Bonus += self.skill_check_condition("crafting")
        Bonus += self.skill_check_traits("crafting")
        Bonus += self.skill_check_equipment("crafting")
        return(Bonus)
        #return(max(0, Bonus))

    

    # Cha
    @property
    def bartering(self):
        Bonus = self.get_skill_mod(self.charisma)
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['bartering']['level'])
        Bonus += self.skill_check_condition("bartering")
        Bonus += self.skill_check_traits("bartering")
        Bonus += self.skill_check_equipment("bartering")
        return(Bonus)
        #return(max(0, Bonus))


    @property
    def persuasion(self):
        Bonus = self.get_skill_mod(int(self.charisma*.75) + int(self.wisdom*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['persuasion']['level'])
        Bonus += self.skill_check_condition("persuasion")
        Bonus += self.skill_check_traits("persuasion")
        Bonus += self.skill_check_equipment("persuasion")
        return(Bonus)
        #return(max(0, Bonus))

    
    @property
    def intimidation(self):
        Bonus = self.get_skill_mod(int(self.charisma*.75) + int(self.strength*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['intimidation']['level'])
        Bonus += self.skill_check_condition("intimidation")
        Bonus += self.skill_check_traits("intimidation")
        Bonus += self.skill_check_equipment("intimidation")
        return(Bonus)
        #return(max(0, Bonus))

    
    @property
    def deception(self):
        Bonus = self.get_skill_mod(int(self.charisma*.75) + int(self.intelligence*.25))
        Bonus += self.skill_level_to_bonus(self.level_tracker.levels['deception']['level'])
        Bonus += self.skill_check_condition("deception")
        Bonus += self.skill_check_traits("deception")
        Bonus += self.skill_check_equipment("deception")
        return(Bonus)
        #return(max(0, Bonus))



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
    
    @property
    def perception(self):
        total = self.base_perception
        total += self.check_condition("perception")
        total += self.check_traits("perception")
        total += self.check_equipment("perception")
        return(max(0, total))





    # Base stat declare
    
    @property
    def base_strength(self):
        return(self.level_tracker.levels['strength']['level'])
        
    @property
    def base_dexterity(self):
        return(self.level_tracker.levels['dexterity']['level'])

    @property
    def base_intelligence(self):
        return(self.level_tracker.levels['intelligence']['level'])

    @property
    def base_wisdom(self):
        return(self.level_tracker.levels['wisdom']['level'])

    @property
    def base_charisma(self):
        return(self.level_tracker.levels['charisma']['level'])
    
    @property
    def base_hp(self):
        return(int(self.level_tracker.levels['base_hp']['level']))
    
    @property
    def base_mp(self):
        return(int(self.level_tracker.levels['base_mp']['level']))
    
    # @property
    # def speed(self):
    #     total = self.base_speed
    #     total += self.check_condition("speed")
    #     total += self.check_traits("speed")
    #     total += self.check_equipment("speed")
    #     return(max(1, total))

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
        if self.owner.traits:
            for trait in self.owner.traits:
                if trait.modifiers.get(stat):
                    total += trait.modifiers.get(stat)
        return(total)

    def check_condition(self, stat):
        total = 0
        if self.owner.conditions:
            for condition in self.owner.conditions:
                if condition.modifiers.get(stat):
                    total += condition.modifiers.get(stat)
        return(total)

    def check_equipment(self, stat):
        total = 0
        if self.owner.inventory:
            for gear_slot in self.owner.inventory.wearing.keys():
                if self.owner.inventory.wearing[gear_slot]:
                    if self.owner.inventory.wearing[gear_slot].stats.get(stat):
                        total += self.owner.inventory.wearing[gear_slot].stats.get(stat)
        return(total)




    # SKILL checks
    # Functions for skills, returns the base modifier without luck or d20
    def skill_check_traits(self, skill):
        total = 0
        if self.owner.traits:
            for trait in self.owner.traits:
                if trait.modifiers.get(skill):
                    total += self.skill_level_to_bonus(trait.modifiers.get(skill))
        return(total)

    def skill_check_condition(self, skill):
        total = 0
        if self.owner.conditions:
            for condition in self.owner.conditions:
                if condition.modifiers.get(skill):
                    total += self.skill_level_to_bonus(condition.modifiers.get(skill))
        return(total)

    def skill_check_equipment(self, skill):
        total = 0
        if self.owner.inventory:
            for gear_slot in self.owner.inventory.wearing.keys():
                if self.owner.inventory.wearing[gear_slot]:
                    if self.owner.inventory.wearing[gear_slot].stats.get(skill):
                        total += self.skill_level_to_bonus(self.owner.inventory.wearing[gear_slot].stats.get(skill))
        return(total)
    




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
                    