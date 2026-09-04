from .equipment import Equipment

class Armor(Equipment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "armor"

WOODEN_ARMOR = Armor(
    "Wooden Armor",
    ["knight"],
    defense_bonus=10,
    max_health_bonus=5
)
