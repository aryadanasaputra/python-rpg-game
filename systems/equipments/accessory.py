from .equipment import Equipment

class Accessory(Equipment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "accessory"

WOODEN_RING = Accessory(
    "Wooden Ring",
    max_mana_bonus=10,
    max_health_bonus=5
)
