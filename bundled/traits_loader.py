from unit_components.trait import trait
from unit_components.damage import Damage


# new_trait = trait(
#     name = "test",
#     shown_name = "test1",
#     item_namechange = [0, "of testing"],
#     duration = duration,
#     on_char = {
#         "skills"              : {}, # "name" : value
#         "stats"               : {}, # "name" : value
#         "resistances"         : {}, # "name" : value
#         "perturn_func"        : [], # <function>, ...
#         "perturn_damage"      : []  # <Damage>, ...
#     },
#     on_item = {
#         "skills"              : {}, # "name" : value
#         "stats"               : {}, # "name" : value
#         "resistances"         : {}, # "name" : value
#         "perturn_func"        : [], # <function>, ...
#         "onhit_damage"        : [], # <Damage>, ...
#         "onhit_enemy_func"    : []  # <function>, ...
#     }
# )


class trait_generator():
    def __init__(self):
        self.traits_generated = 0
        self.traits = ['fire_1', 'fire_2', 'fire_3', 'fire_4']


    def generate(self, name, duration=-1):
        if name == "fire_1":
            new_trait = trait(
                name = "fire_1",
                shown_name = "Fire 1",
                item_namechange = [0, "Warm"],
                duration = duration,
                on_char = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {},
                    "perturn_func" : [],
                    "perturn_damage" : [Damage("1d2", "fire")]
                },
                on_item = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {"fire_resistance" : 2},
                    "perturn_func" : [],
                    "onhit_damage" : [Damage("1d2", "fire")],
                    "onhit_enemy_func"   : []  #TODO Add burning_1(chance=1/5, turns=3) which can apply fire_1 for 3 turns
                }
            )
        
        if name == "fire_2":
            new_trait = trait(
                name = "fire_2",
                shown_name = "Fire 2",
                item_namechange = [0, "Hot"],
                duration = duration,
                on_char = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {},
                    "perturn_func" : [],
                    "perturn_damage" : [Damage("1d4", "fire")]
                },
                on_item = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {"fire_resistance" : 4},
                    "perturn_func" : [],
                    "onhit_damage" : [Damage("1d4", "fire")],
                    "onhit_enemy_func"   : []  #TODO Add burning_1(chance=1/2, turns=4) which can apply fire_1 for 3 turns
                }
            )
        
        if name == "fire_3":
            new_trait = trait(
                name = "fire_3",
                shown_name = "Fire 3",
                item_namechange = [0, "Burning"],
                duration = duration,
                on_char = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {},
                    "perturn_func" : [], #TODO Add smokegen_1()
                    "perturn_damage" : [Damage("2d4", "fire")]
                },
                on_item = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {"fire_resistance" : 5},
                    "perturn_func" : [], #TODO Add smokegen_1()
                    "onhit_damage" : [Damage("2d4", "fire")],
                    "onhit_enemy_func"   : []  #TODO Add burning_2(chance=1/3, turns=3) which can apply fire_2 for 3 turns
                }
            )
        
        if name == "fire_4":
            new_trait = trait(
                name = "fire_4",
                shown_name = "Fire 4",
                item_namechange = [0, "Smoldering"],
                duration = duration,
                on_char = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {},
                    "perturn_func" : [], #TODO Add smokegen_2()
                    "perturn_damage" : [Damage("2d4", "fire")]
                },
                on_item = {
                    "skills" : {},
                    "stats" : {},
                    "resistances" : {"fire_resistance" : 6},
                    "perturn_func" : [], #TODO Add smokegen_2()
                    "onhit_damage" : [Damage("4d4", "fire")],
                    "onhit_enemy_func"   : []  #TODO Add burning_3(chance=1/3, turns=3) which can apply fire_3 for 3 turns
                }
            )
        
        return(new_trait)
