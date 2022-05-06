from random import sample
class Damage:
    def __init__(self, string, type = "pure"):
        self.flat = 0
        self.upper = 0
        self.dice_rolls = 0
        self.name = string
        self.type = type
        self.populate()
    
    def print(self):
        print(self.name, " | ", self.dice_rolls, "d", self.upper, "+", self.flat, sep = "")
    
    def populate(self):
        if 'd' in self.name:
            # See if dice roll in name
            splt = self.name.split("d")
            self.dice_rolls = int(splt[0])
            if "+" in splt[1]:
                splt = splt[1].split("+")
                self.upper = int(splt[0])
                self.flat = int(splt[1])
            elif "-" in splt[1]:
                splt = splt[1].split("-")
                self.upper = int(splt[0])
                self.flat = -1*int(splt[1])
            else:
                self.upper = int(splt[1])
        else:
            self.flat = int(self.name)

    def get_damage(self):
        damage = self.flat
        if self.dice_rolls > 0 and self.upper > 0:
            damage += sum(sample(range(self.upper), self.dice_rolls)) + self.dice_rolls
        return((damage, self.type))
    
    
    @property
    def avg(self):
        total = 0
        total += self.flat
        midx = self.upper/2
        total += midx*self.dice_rolls
        return(total)
