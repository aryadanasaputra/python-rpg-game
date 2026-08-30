class Skill:
    def __init__(self, name, mana_cost, damage=0, heal=0, defense=0, effect=None, effect_target="self"):
        self.name  = name
        self.mana_cost = mana_cost
        self.damage =  damage
        self.heal = heal
        self.defense = defense
        self.effect = effect
        self.effect_target = effect_target
        