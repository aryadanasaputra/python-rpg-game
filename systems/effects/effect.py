class StatusEffect:
    def __init__(self, name, duration, damage=0, defense_bonus=0, attack_bonus=0, health_bonus=0, mana_bonus=0, max_health_bonus=0, max_mana_bonus=0):
        self.name = name
        self.duration = duration
        self.damage = damage
        self.defense_bonus = defense_bonus
        self.attack_bonus = attack_bonus
        self.health_bonus = health_bonus
        self.mana_bonus = mana_bonus
        self.max_health_bonus = max_health_bonus
        self.max_mana_bonus = max_mana_bonus

    def copy(self):
        return StatusEffect(
            self.name,
            self.duration,
            self.damage,
            self.defense_bonus,
            self.attack_bonus,
            self.health_bonus,
            self.mana_bonus,
            self.max_health_bonus,
            self.max_mana_bonus
        )
POISON = StatusEffect("Poison", duration=3, damage=5)
SHIELD = StatusEffect("Shield", duration=3, defense_bonus=5)
WEAKNES = StatusEffect("Weaknes", duration=2, attack_bonus=-2, defense_bonus=-3, max_mana_bonus=-30)
BERSERK = StatusEffect("Berserk", duration=2, attack_bonus=8, defense_bonus=-4)
BURN = StatusEffect("Burning", duration=3, damage=3, defense_bonus=-3)
REGEN = StatusEffect("Regen", duration=2)