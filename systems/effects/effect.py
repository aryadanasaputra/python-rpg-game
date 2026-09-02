class StatusEffect:
    def __init__(self, name, duration, damage=0, defense_bonus=0, attack_bonus=0, health_bonus=0, mana_bonus=0, max_health_bonus=0, max_mana_bonus=0, health_regen=0, mana_regen=0, health_regen_percent=0, mana_regen_percent=0):
        self.name = name
        self.duration = duration
        self.damage = damage
        self.defense_bonus = defense_bonus
        self.attack_bonus = attack_bonus
        self.health_bonus = health_bonus
        self.mana_bonus = mana_bonus
        self.max_health_bonus = max_health_bonus
        self.max_mana_bonus = max_mana_bonus
        self.health_regen = health_regen
        self.mana_regen = mana_regen
        self.health_regen_percent = health_regen_percent
        self.mana_regen_percent = mana_regen_percent
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
            self.max_mana_bonus,
            self.health_regen,
            self.mana_regen,
            self.health_regen_percent,
            self.mana_regen_percent
        )

    def apply_immediate_effect(self, target):
        if self.health_bonus > 0:
            self.restore_health(target, self.health_bonus)
        if self.mana_bonus > 0:
            self.restore_mana(target, self.mana_bonus)

    def process(self, target):
        if not target.life:
            return
        if self.damage > 0:
            print(f"{target.name} takes {self.damage} damage from {self.name}.")
            target.health = max(0, target.health - self.damage)
        if self.health_regen > 0:
            print(f"{target.name} regenerates {self.health_regen} health from {self.name}.")
            self.restore_health(target, self.health_regen)
        if self.mana_regen > 0:
            print(f"{target.name} regenerates {self.mana_regen} mana from {self.name}.")
            self.restore_mana(target, self.mana_regen)
        if self.health_regen_percent > 0:
            regen_amount = int(target.max_health * self.health_regen_percent)
            print(f"{target.name} regenerates {regen_amount} health from {self.name}.")
            self.restore_health(target, regen_amount)
        if self.mana_regen_percent > 0:
            regen_amount = int(target.max_mana * self.mana_regen_percent)
            print(f"{target.name} regenerates {regen_amount} mana from {self.name}.")
            self.restore_mana(target, regen_amount)
            
    def restore_health(self, target, amount):
        old_health = target.health
        target.health = min(target.max_health, target.health + amount)
        restored = target.health - old_health
        print(f"{target.name} gains {restored} health from {self.name}.")

    def restore_mana(self, target, amount):
        old_mana = target.mana
        target.mana = min(target.max_mana, target.mana + amount)
        restored = target.mana - old_mana
        print(f"{target.name} gains {restored} mana from {self.name}." )

# BUFF
SHIELD = StatusEffect(
    "Shield",
    duration=3,
    defense_bonus=5
)

MIGHT = StatusEffect(
    "Might",
    duration=3,
    attack_bonus=5
)

FORTIFY = StatusEffect(
    "Fortify",
    duration=3,
    defense_bonus=8,
    max_health_bonus=20
)

ARCANE_POWER = StatusEffect(
    "Arcane Power",
    duration=3,
    attack_bonus=3,
    max_mana_bonus=30
)

HASTE = StatusEffect(
    "Haste",
    duration=2,
    attack_bonus=4
)

# DEBUFF
WEAKNESS = StatusEffect(
    "Weakness",
    duration=2,
    attack_bonus=-2,
    defense_bonus=-3,
    max_mana_bonus=-30
)

VULNERABLE = StatusEffect(
    "Vulnerable",
    duration=2,
    defense_bonus=-6
)

EXHAUSTED = StatusEffect(
    "Exhausted",
    duration=3,
    attack_bonus=-5
)

FRAGILE = StatusEffect(
    "Fragile",
    duration=2,
    defense_bonus=-5,
    max_health_bonus=-15
)

# DAMAGE OVER TIME
POISON = StatusEffect(
    "Poison",
    duration=3,
    damage=5
)

BURN = StatusEffect(
    "Burning",
    duration=3,
    damage=3,
    defense_bonus=-3
)

BLEEDING = StatusEffect(
    "Bleeding",
    duration=3,
    damage=4,
    defense_bonus=-2
)

# REGENERATION OVER TIME
REGEN = StatusEffect(
    "Regen",
    duration=3,
    health_regen_percent=0.05
)

GREATER_REGEN = StatusEffect(
    "Greater Regen",
    duration=4,
    health_regen_percent=0.10
)

MANA_REGEN = StatusEffect(
    "Mana Regeneration",
    duration=3,
    mana_regen_percent=0.10
)

MANA_BOOST = StatusEffect(
    "Mana Boost",
    duration=3,
    max_mana_bonus=40,
    mana_regen_percent=0.05
)

VITALITY = StatusEffect(
    "Vitality",
    duration=3,
    max_health_bonus=30,
    health_regen_percent=0.05
)

# MIXED EFFECTS
BERSERK = StatusEffect(
    "Berserk",
    duration=3,
    attack_bonus=10,
    defense_bonus=-5
)

BLOOD_RAGE = StatusEffect(
    "Blood Rage",
    duration=3,
    attack_bonus=10,
    defense_bonus=-5
)

STONE_SKIN = StatusEffect(
    "Stone Skin",
    duration=3,
    defense_bonus=12,
    attack_bonus=-3
)
TOXIC_ARMOR = StatusEffect(
    "Toxic Armor",
    duration=3,
    defense_bonus=5,
    damage=2
)
