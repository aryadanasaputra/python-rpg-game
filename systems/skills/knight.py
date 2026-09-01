from .skill import Skill
from systems.effects.effect import WEAKNES, BERSERK, SHIELD, BLEEDING

WIND_SWING = Skill(
    "Wind Swing",
    mana_cost=10,
    damage=30,
    effect=BLEEDING,
    target_type="enemy",
    effect_target="enemy"
)

SHIELD_BASH = Skill(
    "Shield Bash",
    mana_cost=15,
    damage=20,
    target_type="enemy",
    effect_target="enemy"
)

RISING_SHIELD = Skill(
    "Rising Shield",
    mana_cost=10,
    effect=SHIELD,
    effect_target="self"
)

HEAL = Skill(
    "Healing",
    mana_cost=5,
    heal=10,
    effect_target="ally"
)

BERSERK = Skill(
    "Berserk",
    mana_cost=12,
    damage=10,
    effect=BERSERK,
    target_type="enemy",
    effect_target="self"
)

INTIMIDATE = Skill(
    "Intimidate",
    mana_cost=8,
    effect=WEAKNES,
    target_type="enemy"
)