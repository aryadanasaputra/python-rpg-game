class Skill:
    def __init__(self, name, mana_cost, damage=0, heal=0, defense=0, effect=None, target_type="self"):
        self.name  = name
        self.mana_cost = mana_cost
        self.damage =  damage
        self.heal = heal
        self.defense = defense
        self.effect = effect
        self.target_type = target_type
        