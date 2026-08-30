class Item:
    def __init__(self,  name, type, health_restore=0, mana_restore=0):
        self.name = name
        self.type = type
        # self.rarety = rarety
        self.health_restore = health_restore
        self.mana_restore = mana_restore
        
HEALTH_POTION = Item(
    "Health Potion",
    "Potion",
    # "Normal",
    health_restore=25
)
MANA_POTION = Item(
    "Mana Potion",
    "Potion",
    # "Normal",
    mana_restore=25
)