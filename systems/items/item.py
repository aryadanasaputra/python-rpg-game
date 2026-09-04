from systems.effects.effect import (
    POISON,
    SHIELD,
    WEAKNESS,
    BERSERK,
    BURN,
    REGEN,
    BLEEDING,
    MIGHT,
    FORTIFY,
    ARCANE_POWER,
    HASTE,
    VULNERABLE,
    EXHAUSTED,
    FRAGILE,
    GREATER_REGEN,
    MANA_REGEN,
    BLOOD_RAGE,
    STONE_SKIN,
    TOXIC_ARMOR,
    MANA_BOOST,
    VITALITY
)

class Item:
    def __init__(self,  name, type, health_restore=0, mana_restore=0, effect=None, target_type="self"):
        self.name = name
        self.type = type
        # self.rarety = rarety
        self.health_restore = health_restore
        self.mana_restore = mana_restore
        self.effect = effect
        self.target_type = target_type
        
HEALTH_POTION = Item(
    "Health Potion",
    "Potion",
    # "Normal",
    health_restore=25,
    effect=REGEN,
    target_type="ally"
)
MANA_POTION = Item(
    "Mana Potion",
    "Potion",
    # "Normal",
    mana_restore=25
)

MANA_REGEN_POTION = Item(
    "Mana Potion",
    "Potion",
    # "Normal",
    mana_restore=25,
    effect=MANA_REGEN
)