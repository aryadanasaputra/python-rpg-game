class Equipment:
    def __init__(self, name, role, defense_bonus=0, attack_bonus=0, max_mana_bonus=0, max_health_bonus=0):
            self.name = name
            self.role = [r.lower() for r in role]
            self.type = "equipment"
            self.defense_bonus = defense_bonus
            self.attack_bonus = attack_bonus
            self.max_mana_bonus = max_mana_bonus
            self.max_health_bonus = max_health_bonus