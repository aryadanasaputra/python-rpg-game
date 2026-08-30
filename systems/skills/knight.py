from .skill import Skill
from systems.effects.effect import BUFF, POISON, WEAKNES, BERSERK

WIND_SWING = Skill(
    "Wind Swing",
    mana_cost=10,
    damage=30
)

SHIELD_BASH = Skill(
    "Shield Bash",
    mana_cost=15,
    damage=20
)

RISING_SHIELD = Skill(
    "Rising Shield",
    mana_cost=10,
    defense=10,
)

HEAL = Skill(
    "Healing",
    mana_cost=5,
    heal=10
)

BERSERK = Skill(
    "Berserk",
    mana_cost=12,
    damage=5,
    effect=BERSERK,
    effect_target="self"
)

INTIMIDATE = Skill(
    "Intimidate",
    mana_cost=8,
    effect=WEAKNES,
    effect_target="enemy"
)