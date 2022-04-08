class trait():
    def __init__(self, trait_name, duration=-1, is_condition=False, *args, **kwargs):
        self.name = trait_name
        self.modifiers = {}
        self.duration = duration
        self.is_condition = is_condition
        for key in kwargs:
            self.modifiers[key] = kwargs[key]
    
