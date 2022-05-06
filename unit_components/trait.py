
# item_namechange
# [1, " of fire"] 1 means it will be in the second spot, so name + list[1]
# [0, "Burning "] 0 means it will be in the first spot, so list[0] + name
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


class trait():
    def __init__(self, name, shown_name, item_namechange = [0, ''], duration=-1, on_char = {}, on_item = {}):
        self.name = name
        self.shown_name = shown_name
        self.item_namechange = item_namechange
        self.duration = duration
        if duration == -1:
            self.is_condition = True
        self.on_char = on_char
        self.on_item = on_item

# class trait2():
#     def __init__(self, trait_name, item_namechange = [0, ""], duration=-1, is_condition=False, *args, **kwargs):
#         self.name = trait_name
#         self.modifiers = {}
#         self.duration = duration
#         self.is_condition = is_condition
#         for key in kwargs:
#             self.modifiers[key] = kwargs[key]
        
    
