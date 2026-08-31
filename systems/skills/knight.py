from .skill import Skill
from systems.effects.effect import WEAKNES, BERSERK, SHIELD

WIND_SWING = Skill(
    "Wind Swing",
    mana_cost=10,
    damage=30,
    target_type="enemy"
)

SHIELD_BASH = Skill(
    "Shield Bash",
    mana_cost=15,
    damage=20,
    target_type="enemy"
)

RISING_SHIELD = Skill(
    "Rising Shield",
    mana_cost=10,
    effect=SHIELD
)

HEAL = Skill(
    "Healing",
    mana_cost=5,
    heal=10
)

BERSERK = Skill(
    "Berserk",
    mana_cost=12,
    effect=BERSERK
)

INTIMIDATE = Skill(
    "Intimidate",
    mana_cost=8,
    effect=WEAKNES,
    target_type="enemy"
)