import random
from systems.characters.character import Character
from systems.equipments.armor import Armor
from systems.equipments.weapon import Weapon
from systems.equipments.accessory import Accessory

ROLE_STATS = {
    "Knight": {
        "max_health": 25,
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

class Player(Character):
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
        print("===================================")

    def status(self):
        self.health = max(0, self.health)

        if self.health <= 0:
            self.life = False
            return f"{self.name} has died."
        return None

    # PROGRESSION
    def _calculate_stat_growth(self, stat, growth_stat):
        stats = ROLE_STATS[self.role]
        growth  = ROLE_GROWTH[self.role]
        return stats[stat]  + (growth[growth_stat] * (self.level - 1))

    def _calculate_experience_limit(self):
        return int(100 * (1 + (self.level - 1) ** 1.5))

    def gain_experience(self, amount):
        messages = []
        self.experience += amount
        messages.append(f"{self.name} gain {amount} EXP!")
        while self.experience >= self.experience_limit:
            self.experience -= self.experience_limit
            level_message = self.level_up()
            messages.append(level_message)
        return messages

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

        return f"{self.name} has leveled up to level {self.level}!"

    # SKILL
    def learn_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            return f"{self.name} learned {skill.name}"
        else:
            return f"{self.name} already knows {skill.name}"

    def use_skill(self, skill, targets, effect_targets=None):
        if not self.can_use_skill(skill):
            return {"success": False}

        effect_targets = effect_targets if effect_targets is not None else []
        successful_targets = []
        messages = []
            
        self.mana -= skill.mana_cost
        messages.append(f"{self.name} using skill name {skill.name}")

        if skill.damage > 0:
            roll = random.randint(1, 20)
            attack_value = self.attack + skill.damage + roll
            # messages.append(f"{self.name} rolls a {roll} for skill, total value: {attack_value}.")
            for target in targets:
                result = self.resolve_attack(target, attack_value, roll)
                if result != "miss":
                    successful_targets.append(target)

        if skill.defense > 0:
            for target in targets:
                target.defense += skill.defense
                # messages.append(f"{self.name} increases defense by {skill.defense} (now {target.defense}).")

        if skill.heal > 0:
            for target in targets:
                healing = skill.heal
                old_hp = target.health
                target.health = min(target.max_health, target.health + healing)
                actual_healed = target.health - old_hp
                messages.append(f"{self.name} heals {actual_healed} HP (now {target.health}/{target.max_health}).")

        if skill.effect is not None:
            if skill.damage > 0 and skill.effect_target == skill.target_type:
                effect_targets_to_apply = successful_targets
            else:
                effect_targets_to_apply = effect_targets

            messages.extend(self.add_skill_effect(skill, effect_targets_to_apply))
        return {
                "success": True,
                "messages": messages
            }

    def add_skill_effect(self, skill, effect_targets):
        messages = []
        if skill.effect is None:
            return messages
        for target in effect_targets:
            if not target.life:
                messages.append(f"{target.name} is already dead and cannot be affected by {skill.effect.name}.")
                continue

            effect = skill.effect.copy()
            effect.apply_immediate_effect(target)
            messages.extend(target.add_effect(effect))
            # messages.append(f"{target.name} receives {effect.name}")
        return messages

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

        self.equipment[slot] = equipment
        self._apply_equipment_stats(equipment, 1)

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
        print(f"{self.name} equipped {equipment.name}")
        return old_equipment
        
    def _unequip(self, slot):
        equipment = self.equipment[slot]

        if equipment is None:
            print(f"{self.name} isn't wearing anything in {slot}.")
            return None

        self._apply_equipment_stats(equipment, -1)

        self.equipment[slot] = None
        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
        print(f"{self.name} unequipped {equipment.name}")
        return equipment
        


