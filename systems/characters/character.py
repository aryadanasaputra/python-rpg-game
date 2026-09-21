import random

class Character:
    def __init__(self, name, max_health, max_mana, attack, defense):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.attack = attack
        self.defense = defense
        self.effects = []
        self.life = True

    def status(self):
        self.health = max(0, self.health)

        if self.health <= 0:
            self.life = False
            return f"{self.name} has died."

        return None

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

    # COMBAT
    def resolve_attack(self, target, attack_value, roll, miss=4, crit=18):
        if roll < miss:
            return {
                "result": "miss",
                "damage": 0,
                "message": f"{self.name}'s attack missed {target.name}!"
            }
        elif roll <= crit:
            damage = max(1, attack_value - target.defense)
            target.health -= damage
            status = target.status()
            return {
                "result": "hit",
                "damage": damage,
                "status": status,
                "message": f"{self.name} attacks {target.name} and causes {damage} damage."
            }
        elif roll > crit:
            damage = max(1, (attack_value - target.defense) * 2)
            target.health -= damage
            status = target.status()
            return {
                "result": "critical",
                "damage": damage,
                "status": status,
                "message": f"{self.name} lands a critical hit on {target.name} and causes {damage} damage!"
            }
        
    def attack_target(self, target):
        if not self.can_act():
            return False
        if not self.can_target(target):
            return False
        roll = random.randint(1, 20)
        attack_value = self.attack + roll

        result = self.resolve_attack(target, attack_value, roll)
        result["roll"] = roll
        result["attack_value"] = attack_value
        return result

    # COMBAT EFFECT
    def add_effect(self, effect):
        messages = []
        for existing_effect in self.effects:
            if existing_effect.name == effect.name:
                existing_effect.duration += effect.duration
                # messages.append(f"{self.name}'s {effect.name} duration extended by {effect.duration} turns, now {existing_effect.duration} turn left.")
                return messages
        self.effects.append(effect)
        self.apply_effect_stat(effect)
        if effect.attack_bonus > 0:
            messages.append(f"{self.name} is effected by {effect.name} and increases attack by {effect.attack_bonus}.")
        elif effect.attack_bonus < 0:
            messages.append(f"{self.name} is effected by {effect.name} and decreases attack by {effect.attack_bonus}.")

        if effect.defense_bonus > 0:
            messages.append(f"{self.name} is effected by {effect.name} and increases defense by {effect.defense_bonus}.")
        elif effect.defense_bonus < 0:
            messages.append(f"{self.name} is effected by {effect.name} and decreases defense by {effect.defense_bonus}.")

        if effect.max_health_bonus > 0:
            messages.append(f"{self.name} is effected by {effect.name} and increases maximum health by {effect.max_health_bonus}.")

        if effect.max_mana_bonus > 0:
            messages.append(f"{self.name} is effected by {effect.name} and increases maximum mana by {effect.max_mana_bonus}.")
        return messages

    def apply_effect_stat(self, effect):
        attack = self.attack + effect.attack_bonus
        defense = self.defense + effect.defense_bonus
        self.max_health += effect.max_health_bonus
        self.max_mana += effect.max_mana_bonus

        self.defense = max(0, defense)
        self.attack = max(0, attack)
        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)

    def remove_effect_stat(self, effect):
        self.attack -= effect.attack_bonus
        self.defense -= effect.defense_bonus
        self.max_health -= effect.max_health_bonus
        self.max_mana -= effect.max_mana_bonus

        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)

    def remove_effect(self, effect):
        self.remove_effect_stat(effect)
        self.effects.remove(effect)
        return(f"{self.name}'s {effect.name.lower()} has expired.")
    
    def process_effect(self):
        expired = []
        messages = []
        for effect in self.effects:
            messages.extend(effect.process(self))
            effect.duration -= 1
            if effect.duration <= 0:
                expired.append(effect)
            # messages.append(f"{self.name}'s effect {effect.name.lower()} is {effect.duration} turns left.")

        for effect in expired:
            message = self.remove_effect(effect)
            messages.append(message)

        return messages