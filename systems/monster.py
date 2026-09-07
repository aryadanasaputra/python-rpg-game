import random
from systems.effects.effect import POISON

MONSTER_STATS = {
    "Goblin": {
        "max_health": 50,
        "max_mana": 0,
        "attack": 7,
        "defense": 2,
        "monster_effect": POISON,
        "effect_chance": 0.5
    },
    "Slime": {
        "max_health": 20,
        "max_mana": 0,
        "attack": 5,
        "defense": 0
    },
    "Kobold": {
        "max_health": 60,
        "max_mana": 0,
        "attack": 9,
        "defense": 8
    }
}
class Monster:
    def __init__(self, name, level=1, experience_reward=100, gold_reward=10, drop_item=None, drop_chance=0.5, monster_effect=None, effect_chance=0.5):
        self.name = name
        self.level = level

        base = MONSTER_STATS[name]

        scale = 1 + (level - 1) * 0.25

        self.max_health = int(base["max_health"] * scale)
        self.health = self.max_health
        
        self.max_mana = int(base["max_mana"] * scale)
        self.mana = self.max_mana
        
        self.attack_power = int(base["attack"] * scale)
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
        print(f"Attack  : {self.attack_power}")
        print(f"Defense : {self.defense}")
        print(f"Status  : {'Life' if self.life else 'Dead'}")
        print("====================================")

    def status(self):
        self.health = max(0, self.health)
    
        if self.health <= 0:
            self.life = False
            print(f"{self.name} has died.")

    def get_drop(self):
        if self.drop_item is None:
            return None
        if random.random() <= self.drop_chance:
            return self.drop_item
        return None

    def resolve_attack(self, player, attack_value, roll,  miss=5, crit=18):
        if roll < miss:
            print(f"{self.name}'s attack missed!")
            return
        elif roll <= crit:
            damage = max(1, attack_value - player.defense)
            player.health -= damage
            print(f"{self.name} attacks {player.name} and causes {damage} damage!")
            self.attack_effect(player)
            player.status()
        else:
            damage = max(1,(attack_value - player.defense) * 2)
            player.health -= damage
            print(f"{self.name} lands a critical hit on {player.name} and causes {damage} damage!")
            self.attack_effect(player)
            player.status()

    def attack(self, player):
        if not self.life:
            return
        if not player.life:
            return

        roll = random.randint(1, 20)
        attack_value = self.attack_power + roll
        self.resolve_attack(player, attack_value, roll)

    def attack_effect(self, player):
        if self.monster_effect is None:
            return
        if not player.life:
            return
        if random.random() <= self.effect_chance:
            effect = self.monster_effect.copy()
            effect.apply_immediate_effect(player)
            player.add_effect(effect)

    def add_effect(self, effect):
        for existing_effect in self.effects:
            if existing_effect.name == effect.name:
                existing_effect.duration += effect.duration
                print(f"{self.name}'s {effect.name} duration extended by {effect.duration} turns.")
                return
        self.effects.append(effect)
        self.apply_effect_stat(effect)
        print(f"{self.name} is effected by {effect.name}")
        if effect.attack_bonus > 0:
            print(f"{self.name} increases attack by {effect.attack_bonus}.")
        elif effect.attack_bonus < 0:
            print(f"{self.name} decreases attack by {effect.attack_bonus}.")

        if effect.defense_bonus > 0:
            print(f"{self.name} increases defense by {effect.defense_bonus}.")
        elif effect.defense_bonus < 0:
            print(f"{self.name} decreases defense by {effect.defense_bonus}.")

        if effect.max_health_bonus > 0:
            print(f"{self.name} increases maximum health by {effect.max_health_bonus}.")
        if effect.max_mana_bonus > 0:
            print(f"{self.name} increases maximum mana by {effect.max_mana_bonus}.")

    def apply_effect_stat(self, effect):
        attack = self.attack_power + effect.attack_bonus
        defense = self.defense + effect.defense_bonus
        self.max_health += effect.max_health_bonus
        self.max_mana += effect.max_mana_bonus

        self.defense = max(0, defense)
        self.attack_power = max(0, attack)
        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)

    def remove_effect_stat(self, effect):
        self.attack_power -= effect.attack_bonus
        self.defense -= effect.defense_bonus
        self.max_health -= effect.max_health_bonus
        self.max_mana -= effect.max_mana_bonus

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)

    def remove_effect(self, effect):
        self.remove_effect_stat(effect)
        self.effects.remove(effect)
        print(f"{self.name}'s {effect.name.lower()} has expired.")
    
    def process_effect(self):
        expired = []
        for effect in (self.effects):
            effect.process(self)
            effect.duration -= 1
            if effect.duration <= 0:
                expired.append(effect)

        for effect in (expired):
            self.remove_effect(effect)

