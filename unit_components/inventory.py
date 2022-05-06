from tcod import gold


class Inventory:
    def __init__(self, gold=0):
        self.gold = gold
        self.Duel_Wield = False
        self.wearing = {
            "Head" : None,
            "Neck" : None,
            "Chest" : None, 
            "Back" : None,
            "Left Arm" : None,
            "Right Arm" : None,
            "Left Hand" : None,
            "Right Hand" : None,
            "Left Ring" : None,
            "Right Ring" : None,
            "Belt" : None,
            "Legs" : None,
            "Left Foot" : None,
            "Right Foot" : None
        }
        self.bag = {
            "Head" : [],
            "Neck" : [],
            "Chest" : [],
            "Back" : [],
            "Arm" : [],
            "Weapon" : [],
            "Rings" : [],
            "Belt" : [],
            "Legs" : [],
            "Feet" : [],
            "Item" : []
        }


    @property
    def gear_worth(self):
        value = 0    
        for key in self.wearing.keys():
            if self.wearing[key] is not None:
                value += self.wearing[key].value
        return(value)

    @property
    def bag_worth(self):
        value = 0
        for key in self.bag.keys():
            for itm in self.bag[key]:
                value += itm.value * itm.quantity
        value += self.gear_worth
        return(value)

    def get_item(self, got_item):
        got_item.owner = self.owner
        # Check bag for any pre-existing of this item
        # if already had, add duplicate
        for item in self.bag[got_item.type]:
            if item.t_name == got_item.t_name:
                item.quantity += got_item.quantity
                return None
        self.bag[got_item.type].append(got_item)
        return None

    def unequip_item(self, position):
        # removes item from slot and puts in bag
        self.get_item(self.wearing[position])
        self.wearing[position] = None

    def equip_item(self, e_item, position=None):
        # Requires Position if One Hand
        if e_item.type == "Weapon":
            if e_item.twohand:
                # Two hand weapon, remove stuff from hands
                # You duelwield with your right hand
                if self.wearing['Left Hand'] != None:
                    self.get_item(self.wearing['Left Hand'])
                    self.wearing['Left Hand'] = None
                if self.wearing['Right Hand'] != None:
                    self.get_item(self.wearing['Right Hand'])
                self.wearing["Right Hand"] = e_item.copy_self(1)
                e_item.quantity -= 1
                if e_item.quantity <= 0:
                    self.bag[e_item.type].remove(e_item)
                self.Duel_Wield = True
                return None
            else:
                if self.Duel_Wield:
                    self.Duel_Wield = False
                    self.get_item(self.wearing['Right Hand'])
                    self.wearing['Right Hand'] = None
                    

        if position == None:
            position = e_item.type
            
        if self.wearing[position] == None:
            # not wearing something
            self.wearing[position] = e_item.copy_self(1)
            e_item.quantity -= 1
            if e_item.quantity <= 0:
                self.bag[e_item.type].remove(e_item)
        else: 
            # Swap
            self.get_item(self.wearing[position])
            self.wearing[position] = e_item.copy_self(1)
            e_item.quantity -= 1
            if e_item.quantity <= 0:
                self.bag[e_item.type].remove(e_item)
        
