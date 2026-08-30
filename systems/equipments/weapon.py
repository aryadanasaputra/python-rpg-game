from .equipment import Equipment

class Weapon(Equipment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "accessory"

WOODEN_LONG_SWORD = Weapon(
    "Wooden Long Sword",
    attack_bonus=10
)
LEGENDARY_LONG_SWORD = Weapon(
    "Legenday Long Sword",
    attack_bonus=250,
    max_mana_bonus=50
)