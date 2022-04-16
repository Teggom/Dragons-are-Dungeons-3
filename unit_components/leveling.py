class level_tracker():
    def __init__(self, exp_mod_stat = 1.5, exp_base_stat = 10, exp_mod_skill = 4, exp_base_skill = 80, *args, **kwargs):

        self.exp_mod_stat = exp_mod_stat
        self.exp_base_stat = exp_base_stat
        self.exp_mod_skill = exp_mod_skill
        self.exp_base_skill = exp_base_skill

        self.levels = {}

        to_create_stat = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma']

        to_create_skill = ['athletics', 'acrobatics', 'slight_of_hand', 'stealth', 
            'arcana', 'alchemy', 'crafting', 'bartering', 'persuasion', 
            'intimidation', 'deception']
        
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

    def add_exp(self, stat_or_skill, exp):
        self.levels[stat_or_skill]['exp'] += exp
        if self.levels[stat_or_skill]['exp'] >= self.levels[stat_or_skill]['exp_cap']:
            print('{} Leveled Up! {} -> {}'.format(stat_or_skill, self.levels[stat_or_skill]['level'], self.levels[stat_or_skill]['level']+1))
            self.levels[stat_or_skill]['level'] += 1
            self.levels[stat_or_skill]['exp'] = self.levels[stat_or_skill]['exp'] % self.levels[stat_or_skill]['exp_cap']
            if self.levels[stat_or_skill]['type'] == 'stat':
                self.levels[stat_or_skill]['exp_cap'] = self.exp_base_stat + int(self.levels[stat_or_skill]['level']**self.exp_mod_stat)
            else:
                self.levels[stat_or_skill]['exp_cap'] = self.exp_base_skill + int(self.levels[stat_or_skill]['level']**self.exp_mod_skill)
