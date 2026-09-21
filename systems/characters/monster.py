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
        self.name = name
        self.level = level

        base = MONSTER_STATS[name]

        scale = 1 + (level - 1) * 0.25

        self.max_health = int(base["max_health"] * scale)
        self.health = self.max_health
        
        self.max_mana = int(base["max_mana"] * scale)
        self.mana = self.max_mana
        
        self.attack = int(base["attack"] * scale)
        self.defense = int(base["defense"] * scale)
        self.experience_reward = int(experience_reward * scale)
        self.gold_reward = int(gold_reward * scale)
        self.drop_item = drop_item
        self.drop_chance = drop_chance

        self.monster_effect = base.get("monster_effect")
        self.effect_chance = base.get("effect_chance")
        self.reward_given = False

        self.effects = []

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

    def resolve_attack(self, player, attack_value, roll,  miss=5, crit=18):
        if roll < miss:
            return {
                "result": "miss",
                "damage": 0,
                "message": f"{self.name}'s attack missed {player.name}!"
            }
        elif roll <= crit:
            damage = max(1, attack_value - player.defense)
            player.health -= damage
            print(f"{self.name} attacks {player.name} and causes {damage} damage!")
            self.attack_effect(player)
            status = player.status()
            return {
                "result": "hit",
                "damage": damage,
                "status": status,
                "message": f"{self.name} attacks {player.name} and causes {damage} damage."
            }
            
        else:
            damage = max(1,(attack_value - player.defense) * 2)
            player.health -= damage
            print(f"{self.name} lands a critical hit on {player.name} and causes {damage} damage!")
            status = player.status()
            return {
                "result": "critical",
                "damage": damage,
                "status": status,
                "message": f"{self.name} lands a critical hit on {player.name} and causes {damage} damage!"
            }

    def attack_target(self, player):
        if not self.life:
            return
        if not player.life:
            return

        roll = random.randint(1, 20)
        attack_value = self.attack + roll
        result = self.resolve_attack(player, attack_value, roll)
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

