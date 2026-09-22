import random
from systems.characters.character import Character
from systems.effects.effect import POISON, BLEEDING

MONSTER_STATS = {
    "Goblin": {
        "max_health": 50,
        "max_mana": 0,
        "attack": 7,
        "defense": 2,
        "monster_effect": POISON,
        "effect_chance": 0.3
    },
    "Slime": {
        "max_health": 20,
        "max_mana": 0,
        "attack": 5,
        "defense": 0,
        "monster_effect": POISON,
        "effect_chance": 0.5
    },
    "Kobold": {
        "max_health": 60,
        "max_mana": 0,
        "attack": 9,
        "defense": 8,
        "monster_effect": BLEEDING,
        "effect_chance": 0.6
    }
}
class Monster(Character):
    def __init__(self, name, level=1, experience_reward=100, gold_reward=10, drop_item=None, drop_chance=0.5, monster_effect=None, effect_chance=0.5):
        self.level = level

        base = MONSTER_STATS[name]

        scale = 1 + (level - 1) * 0.25

        self.max_health = int(base["max_health"] * scale)
        # self.health = self.max_health
        
        self.max_mana = int(base["max_mana"] * scale)
        # self.mana = self.max_mana
        
        self.attack = int(base["attack"] * scale)
        self.defense = int(base["defense"] * scale)
        super().__init__(name, self.max_health, self.max_mana, self.attack, self.defense)
        self.experience_reward = int(experience_reward * scale)
        self.gold_reward = int(gold_reward * scale)
        self.drop_item = drop_item
        self.drop_chance = drop_chance

        self.monster_effect = base.get("monster_effect")
        self.effect_chance = base.get("effect_chance")
        self.reward_given = False

        self.skills = []

        self.life = True

    def info(self):
        print("\n========== MONSTER STATUS ==========")
        print(f"Name    : {self.name}")
        print(f"Level   : {self.level}")
        print(f"Health  : {self.health}/{self.max_health}")
        print(f"Mana    : {self.mana}/{self.max_mana}")
        print(f"Attack  : {self.attack}")
        print(f"Defense : {self.defense}")
        print(f"Status  : {'Life' if self.life else 'Dead'}")
        print("====================================")

    def get_drop(self):
        if self.drop_item is None:
            return None
        if random.random() <= self.drop_chance:
            return self.drop_item
        return None

    def attack_target(self, player):
        result = super().attack_target(player)
        if result is None:
            return None
        if not self.life:
            return result
        if not player.life:
            return result

        if result["result"] != "miss":
            self.attack_effect(player)
        return result

    def attack_effect(self, player):
        if self.monster_effect is None:
            return
        if not player.life:
            return
        if random.random() <= self.effect_chance:
            effect = self.monster_effect.copy()
            effect.apply_immediate_effect(player)
            player.add_effect(effect)

