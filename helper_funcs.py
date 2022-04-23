def get_items_at_loc(game, x, y):
    items_here = []
    for item in game['items']:
        if item.x == x and item.y == y:
            items_here.append(item)
    return(items_here)

def gear_lookup(slot_name):
    # Given a slotname ("Right Foot") returns the associated bag name ("Feet")
    if slot_name in ["Head", "Neck", "Chest", "Back", "Belt", "Legs"]:
        return slot_name
    if slot_name == "Left Arm" or slot_name == "Right Arm":
        return "Arm"
    if slot_name == "Left Hand" or slot_name == "Right Hand":
        return "Weapon"
    if slot_name == "Left Foot" or slot_name == "Right Foot":
        return "Feet"
    if slot_name == 'Left Ring' or slot_name == "Right Ring":
        return 'Rings'
    

