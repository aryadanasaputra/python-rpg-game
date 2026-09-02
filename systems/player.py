import random
from systems.equipments.armor import Armor
from systems.equipments.weapon import Weapon
from systems.equipments.accessory import Accessory

ROLE_STATS = {
    "Knight": {
        "max_health": 125,
        "max_mana": 25,
        "attack": 15,
        "defense": 10
    },
    "Mage": {
        "max_health": 80,
        "max_mana": 100,
        "attack": 10,
        "defense": 3
    },
    "Archer": {
        "max_health": 90,
        "max_mana": 30,
        "attack": 20,
        "defense": 5
    }
}

ROLE_GROWTH = {
    "Knight": {
        "health": 15,
        "mana": 3,
        "attack": 2,
        "defense": 5
    },
    "Mage": {
        "health": 7,
        "mana": 15,
        "attack": 4,
        "defense": 2
    },
    "Archer": {
        "health": 8,
        "mana": 6,
        "attack": 7,
        "defense": 3
    }
}

class Character:
    def __init__ (self, name, role, level=1, experience=0, experience_reward=0):
        self.name = name
        self.role = role
        self.level = level

        self.max_health = self._calculate_stat_growth("max_health", "health")
        self.health = self.max_health

        self.max_mana = self._calculate_stat_growth("max_mana", "mana")
        self.mana = self.max_mana

        self.attack = self._calculate_stat_growth("attack", "attack")
        self.defense = self._calculate_stat_growth("defense", "defense")
        self.equipment = {
            "weapon" : None,
            "armor" : None,
            "accessory" : None}

        self.skills = []
        self.inventory = {}
        self.gold = 0

        self.experience = experience
        self.experience_limit = self._calculate_experience_limit()
        self.experience_reward = experience_reward

        self.effects = []

        self.life = True

    # INFORMATION
    def info(self):
        print("\n========== PLAYER STATUS ==========")
        print(f"Name    : {self.name}")
        print(f"Role    : {self.role}")
        print(f"Level   : {self.level}")
        print(f"Health  : {self.health}/{self.max_health}")
        print(f"Mana    : {self.mana}/{self.max_mana}")
        print(f"EXP     : {self.experience}/{self.experience_limit}")
        print(f"Attack  : {self.attack}")
        print(f"Defense : {self.defense}")
        skills_text = ', '.join(skill.name for skill in self.skills) if self.skills else "-"
        print(f"Skill   : {skills_text}")
        print(f"Status  : {'Life' if self.life else 'Dead'}")
        print(f"Gold    : {self.gold} $")
        print("===================================")

    def status(self):
        self.health = max(0, self.health)

        if self.health <= 0:
            self.life = False
            print(f"{self.name} has died.")

    # PROGRESSION
    def _calculate_stat_growth(self, stat, growth_stat):
        stats = ROLE_STATS[self.role]
        growth  = ROLE_GROWTH[self.role]
        return stats[stat]  + (growth[growth_stat] * (self.level - 1))

    def _calculate_experience_limit(self):
        return int(100 * (1 + (self.level - 1) ** 1.5))

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gain {amount} EXP!")
        while self.experience >= self.experience_limit:
            self.experience -= self.experience_limit
            self.level_up()

    def level_up(self):
        growth  = ROLE_GROWTH[self.role]
        self.level += 1

        self.max_health += growth["health"]
        self.health =  self.max_health

        self.max_mana += growth["mana"]
        self.mana = self.max_mana

        self.attack += growth["attack"]
        self.defense += growth["defense"]

        self.experience_limit = self._calculate_experience_limit()

        print(f"{self.name} has leveled up to level {self.level}!")

    # VALIDATION
    def can_act(self):
        if not self.life:
            print(f"{self.name} is dead and cannot act!")
            return False
        return True

    def can_target(self, target):
        if not target.life:
            print(f"{target.name} is already dead... ")
            return False
        return True

    def knows_skill(self, skill):
        if skill not in self.skills:
            print(f"{self.name} doesn't know {skill.name}.")
            return False
        return True

    def can_use_mana(self, skill):
        if self.mana < skill.mana_cost:
            print(f"{self.name} doesn't have enough mana!")
            return False
        return True

    def can_use_skill(self, skill):
        if not self.can_act():
            return False
        if not self.knows_skill(skill):
            return False
        if not self.can_use_mana(skill):
            return False
        
        return True

    # SKILL
    def learn_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            print(f"{self.name} learned {skill.name}")
        else:
            print(f"{self.name} already knows {skill.name}")

    def use_skill(self, skill, targets, effect_targets=None):
        if not self.can_use_skill(skill):
            return False

        effect_targets = effect_targets if effect_targets is not None else []
        successful_targets = []
            
        self.mana -= skill.mana_cost
        print(f"{self.name} using skill name {skill.name}")

        if skill.damage > 0:
            roll = random.randint(1, 20)
            attack_value = self.attack + skill.damage + roll
            print(f"{self.name} rolls a {roll} for skill, total value: {attack_value}.")
            for target in targets:
                result = self.resolve_attack(target, attack_value, roll)
                if result != "miss":
                    successful_targets.append(target)

        if skill.defense > 0:
            for target in targets:
                target.defense += skill.defense
                print(f"{self.name} increases defense by {skill.defense} (now {target.defense}).")
                successful_targets.append(target)

        if skill.heal > 0:
            for target in targets:
                healing = skill.heal
                old_hp = target.health
                target.health = min(target.max_health, target.health + healing)
                actual_healed = target.health - old_hp
                print(f"{self.name} heals {actual_healed} HP (now {target.health}/{target.max_health}).")
                successful_targets.append(target)

        self.add_skill_effect(skill, skill.effect, effect_targets)
        return True

    def add_skill_effect(self, skill, effect, effect_targets):
        if skill.effect is None:
            return
        for target in effect_targets:
            if not target.life:
                print(f"{target.name} is already dead and cannot be affected by {skill.effect.name}.")
                continue

            effect = skill.effect.copy()
            effect.apply_immediate_effect(target)
            target.add_effect(effect)

    # INVENTORY
    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        print(f"{self.name} obtained {item.name}")

    def use_item(self, item):
        if not self.can_act():
            return False
        if item not in self.inventory:
            print(f"{self.name} doesn't have {item.name}.")
            return False

        if item.type.lower() == "potion":
            print(f"{self.name} uses {item.name}")
            old_health = self.health
            old_mana = self.mana
            self.health = min(self.max_health,self.health + item.health_restore)
            self.mana = min(self.max_mana,self.mana + item.mana_restore)
            actual_health = self.health - old_health
            actual_mana = self.mana - old_mana
            if item.health_restore > 0:
                print(f"{self.name} restored {actual_health} HP.")
            if item.mana_restore > 0:
                print(f"{self.name} restored {actual_mana} MP.")
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                del self.inventory[item]
            return True
        elif isinstance(item, Armor):
            self.equip_armor(item)
        elif isinstance(item, Weapon):
            self.equip_weapon(item)
        elif isinstance(item, Accessory):
            self.equip_accessory(item)
        return False

    def add_gold(self, amount):
        self.gold += amount
        print(f"{self.name} obtained {amount} Gold!")

    # EQUIPMENT
    def _apply_equipment_stats(self, equipment, multiplier):
        self.attack += equipment.attack_bonus * multiplier
        self.defense += equipment.defense_bonus * multiplier
        self.max_health += equipment.max_health_bonus * multiplier
        self.max_mana += equipment.max_mana_bonus * multiplier

    def _equip(self, slot, equipment):
        old_equipment = self.equipment[slot]

        if old_equipment:
            self._apply_equipment_stats(old_equipment, -1)
            self.add_item(old_equipment)

        self.equipment[slot] = equipment
        self._apply_equipment_stats(equipment, 1)

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
        print(f"{self.name} equipped {equipment.name}")

    def equip(self, item):
        if item not in self.inventory:
            print(f"{self.name} doesn't have {item.name}")
            return False
        
        if isinstance(item, Armor):
            self._equip("armor", item)
        elif isinstance(item, Accessory):
            self._equip("accessory", item)
        elif isinstance(item, Weapon):
            self._equip("weapon", item)
        else:
            print(f"{item.name} is not an equipment.")
            return False
        
        self.inventory[item] -= 1
        if self.inventory[item] <= 0:
            del self.inventory[item]

        return True
        

    def _unequip(self, slot):
        equipment = self.equipment[slot]

        if equipment is None:
            print(f"{self.name} isn't wearing anything in {slot}.")
            return False

        self._apply_equipment_stats(equipment, -1)

        self.equipment[slot] = None
        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
        self.add_item(equipment)
        print(f"{self.name} unequipped {equipment.name}")
        return True

    def equip_armor(self, armor):
        self._equip("armor", armor)

    def unequip_armor(self):
        self._unequip("armor")

    def equip_weapon(self, weapon):
        self._equip("weapon", weapon)

    def unequip_weapon(self):
        self._unequip("weapon")

    def equip_accessory(self, accessory):
        self._equip("accessory", accessory)
    
    def unequip_accessory(self):
        self._unequip("accessory")
        
    # COMBAT
    def resolve_attack(self, target, attack_value, roll, miss=4, crit=18):
        if roll < miss:
            print(f"{self.name}'s attack missed {target.name}!")
            return "miss"
        elif roll <= crit:
            damage = max(1, attack_value - target.defense)
            target.health -= damage
            print(f"{self.name} attacks {target.name} and causes {damage} damage.")
            target.status()
            return "hit"
        elif roll > crit:
            damage = max(1, (attack_value - target.defense) * 2)
            target.health -= damage
            print(f"{self.name} lands a critical hit on {target.name} and causes {damage} damage!")
            target.status()
            return "critical"

    def attack_target(self, target):
        if not self.can_act():
            return False
        if not self.can_target(target):
            return False
        roll = random.randint(1, 20)
        attack_value = self.attack + roll
        print(f"{self.name} rolls a {roll} for attack, total attack value: {attack_value}.")
        self.resolve_attack(target, attack_value, roll)
        return True

    # COMBAT EFFECT
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
        if effect.defense_bonus > 0:
            print(f"{self.name} increases defense by {effect.defense_bonus}.")
        if effect.max_health_bonus > 0:
            print(f"{self.name} increases maximum health by {effect.max_health_bonus}.")
        if effect.max_mana_bonus > 0:
            print(f"{self.name} increases maximum mana by {effect.max_mana_bonus}.")

    def apply_effect_stat(self, effect):
        self.attack += effect.attack_bonus
        self.defense += effect.defense_bonus
        self.max_health += effect.max_health_bonus
        self.max_mana += effect.max_mana_bonus

        if effect.max_health_bonus > 0:
            self.health = max(self.health, int(self.max_health * 0.9))
        elif effect.max_health_bonus < 0:
            self.health = min(self.health, self.max_health)

        if effect.max_mana_bonus > 0:
            self.mana = max(self.mana, int(self.max_mana * 0.9))
        elif effect.max_mana_bonus < 0:
            self.mana = min(self.mana, self.max_mana)

    def remove_effect_stat(self, effect):
        self.attack -= effect.attack_bonus
        self.defense -= effect.defense_bonus
        self.max_health -= effect.max_health_bonus
        self.max_mana -= effect.max_mana_bonus

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
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
            self.remove_effect_stat(effect)


