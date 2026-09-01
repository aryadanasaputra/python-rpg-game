from .skill import Skill
from systems.effects.effect import BURN, REGEN

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
    effect=REGEN,
    effect_target="ally"
)