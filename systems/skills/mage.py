from .skill import Skill
from systems.effects.effect import BURN, HEAL

IGNITE = Skill(
    "Ignite",
    mana_cost=10,
    damage=10,
    effect=BURN,
    effect_target="enemy"
)

IGNITE = Skill(
    "Ignite",
    mana_cost=10,
    damage=10,
    effect=BURN,
    effect_target="enemy"
)

HEALING = Skill(
    "Healing",
    mana_cost=15,
    effect=HEAL
)