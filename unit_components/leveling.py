class level_tracker():
    def __init__(self, exp_mod_stat = 1.5, exp_base_stat = 10, exp_mod_skill = 4, exp_base_skill = 80, exp_mod_weapon = 3, exp_base_weapon = 150, *args, **kwargs):

        self.exp_mod_stat = exp_mod_stat
        self.exp_base_stat = exp_base_stat
        self.exp_mod_skill = exp_mod_skill
        self.exp_base_skill = exp_base_skill
        self.exp_mod_weapon = exp_mod_weapon
        self.exp_base_weapon = exp_base_weapon

        self.hp_exp = 30
        self.hp_base = 1.4

        self.mp_exp = 20
        self.mp_base = 1.3

        self.levels = {}

        to_create_stat = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma']

        to_create_skill = ['athletics', 'acrobatics', 'slight_of_hand', 'stealth', 
            'arcana', 'alchemy', 'crafting', 'bartering', 'persuasion', 
            'intimidation', 'deception', 'mining', 'enchanting', 'harvesting', 'summoning']

        to_create_weapon = [
            'sword', 'dagger', 'greatsword', 'axe', 'hammer', 'whip',
            'greatshield', 'flail', 'spear', 'halberd', 'scythe',
            'fist', 'bow', 'crossbow', 'staff', 'wand'
        ]
        
        for stat in to_create_stat:
            if stat in kwargs:
                self.levels[stat] = {
                    "level" : kwargs[stat],
                    "type" : "stat",
                    "exp"   : 0,
                    "exp_cap" : self.exp_base_stat + int(kwargs[stat]**self.exp_mod_stat)
                }
            else:
                self.levels[stat] = {
                    "level" : 1,
                    "type" : "stat",
                    "exp"   : 0,
                    "exp_cap" : self.exp_base_stat 
                }
            
        
        for skill in to_create_skill:
            if skill in kwargs:
                self.levels[skill] = {
                    "level" : kwargs[skill],
                    "type" : "skill",
                    "exp" : 0,
                    "exp_cap" : self.exp_base_skill + int(kwargs[skill]**self.exp_mod_skill)
                }
            else:
                self.levels[skill] = {
                    "level" : 0,
                    "type" : "skill",
                    "exp" : 0,
                    "exp_cap" : self.exp_base_skill 
                }
        
        for weapon_level in to_create_weapon:
            if weapon_level in kwargs:
                self.levels[weapon_level] = {
                    "level" : kwargs[weapon_level],
                    "type" : "weapon",
                    "exp" : 0,
                    "exp_cap" : self.exp_base_skill + int(kwargs[weapon_level]**self.exp_mod_skill)
                }
            else:
                self.levels[weapon_level] = {
                    "level" : 0,
                    "type" : "weapon_",
                    "exp" : 0,
                    "exp_cap" : self.exp_base_skill 
                }
        
        if 'base_hp' in kwargs:
            self.levels['base_hp'] = {
                'level' : kwargs['base_hp'],
                'type' : 'base_hp',
                'exp' : 0,
                'exp_cap' : self.hp_base + int(kwargs['base_hp']**self.hp_exp)
            }
        else:
            self.levels['base_hp'] = {
                'level' : 30,
                'type' : 'base_hp',
                'exp' : 0,
                'exp_cap' : self.hp_base + int(30**self.hp_exp)
            }
        
        if 'mp' in kwargs:
            self.levels['base_mp'] = {
                'level' : kwargs['base_mp'],
                'type' : 'base_mp',
                'exp' : 0,
                'exp_cap' : self.mp_base + int(kwargs['base_mp']**self.mp_exp)
            }
        else:
            self.levels['base_mp'] = {
                'level' : 30,
                'type' : 'base_mp',
                'exp' : 0,
                'exp_cap' : self.mp_base + int(30**self.mp_exp)
            }

        

    def add_exp(self, stat_or_skill, exp):
        self.levels[stat_or_skill]['exp'] += exp
        if self.levels[stat_or_skill]['exp'] >= self.levels[stat_or_skill]['exp_cap']:
            print('{} Leveled Up! {} -> {}'.format(stat_or_skill, self.levels[stat_or_skill]['level'], self.levels[stat_or_skill]['level']+1))
            self.levels[stat_or_skill]['level'] += 1
            self.levels[stat_or_skill]['exp'] = self.levels[stat_or_skill]['exp'] % self.levels[stat_or_skill]['exp_cap']
            if self.levels[stat_or_skill]['type'] == 'stat':
                self.levels[stat_or_skill]['exp_cap'] = self.exp_base_stat + int(self.levels[stat_or_skill]['level']**self.exp_mod_stat)
            elif self.levels[stat_or_skill]['type'] == 'skill':
                self.levels[stat_or_skill]['exp_cap'] = self.exp_base_skill + int(self.levels[stat_or_skill]['level']**self.exp_mod_skill)
            elif self.levels[stat_or_skill]['type'] == 'base_hp':
                self.levels[stat_or_skill]['exp_cap'] = self.hp_base + int(self.levels[stat_or_skill]['level']**self.hp_exp)
            elif self.levels[stat_or_skill]['type'] == 'base_mp':
                self.levels[stat_or_skill]['exp_cap'] = self.mp_base + int(self.levels[stat_or_skill]['level']**self.mp_exp)
