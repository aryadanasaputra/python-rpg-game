from .skill import Skill
from systems.effects.effect import (
    POISON,
    SHIELD,
    WEAKNESS,
    BERSERK,
    BURN,
    REGEN,
    BLEEDING,
    MIGHT,
    FORTIFY,
    ARCANE_POWER,
    HASTE,
    VULNERABLE,
    EXHAUSTED,
    FRAGILE,
    GREATER_REGEN,
    MANA_REGEN,
    BLOOD_RAGE,
    STONE_SKIN,
    TOXIC_ARMOR,
    MANA_BOOST,
    VITALITY
)

IGNITE = Skill(
    "Ignite",
    mana_cost=10,
    damage=10,
    effect=BURN,
    target_type="enemy",
    effect_target="enemy"
)

FLAME_STRIKE = Skill(
    "Flame Strike",
    mana_cost=20,
    damage=10,
    effect=BURN,
    target_type="all_enemies",
    effect_target="all_enemies"
)

HEALING = Skill(
    "Healing",
    mana_cost=15,
    heal=15,
    effect=REGEN,
    target_type="ally",
    effect_target="ally"
)

GREATER_HEALING = Skill(
    "Greater Healing",
    mana_cost=50,
    heal=25,
    effect=GREATER_REGEN,
    target_type="all_allies",
    effect_target="all_allies"
)