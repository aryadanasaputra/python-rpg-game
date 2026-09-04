from systems.equipments.armor import Armor
from systems.equipments.weapon import Weapon
from systems.equipments.accessory import Accessory

class Party:
    def __init__(self, characters):
        self.characters = characters
        self.inventory = {}
        self.gold = 0

    def info(self):
        for i, character in enumerate(self.characters, start=1):
            print(f"{i}. {character.name} ({character.role})\n"
                  f"   - Level  : {character.level}\n"
                  f"   - Health : {character.health}/{character.max_health}\n"
                  f"   - Mana   : {character.mana}/{character.max_mana}")

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        print(f"Party obtained {item.name}")

    def use_item(self, item, character):
        if item not in self.inventory:
            print(f"Party doesn't have {item.name}.")
            return False

        if item.type.lower() == "potion":
            print(f"{character.name} uses {item.name}")
            old_health = character.health
            old_mana = character.mana
            character.health = min(character.max_health,character.health + item.health_restore)
            character.mana = min(character.max_mana,character.mana + item.mana_restore)
            actual_health = character.health - old_health
            actual_mana = character.mana - old_mana

            if item.health_restore > 0:
                print(f"{character.name} restored {actual_health} HP.")

            if item.mana_restore > 0:
                print(f"{character.name} restored {actual_mana} MP.")

            self.inventory[item] -= 1

            if self.inventory[item] <= 0:
                del self.inventory[item]
            print(f"{character.name} used {item.name}")
            return True
            
        return False

    def add_gold(self, amount):
        self.gold += amount
        print(f"Party obtained {amount} Gold!")

    def show_inventory(self):
        print("\n========== PARTY INVENTORY ==========")
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for item, quantity in self.inventory.items():
                print(f"{item.name} x{quantity}")
        print("=====================================")

    def equip(self, character, item):
        if item not in self.inventory:
            print(f"Party doesn't have {item.name}.")
            return False

        if isinstance(item, Armor):
            slot = "armor"
        elif isinstance(item, Weapon):
            slot = "weapon"
        elif isinstance(item, Accessory):
            slot = "accessory"
        else:
            print(f"{item.name} is not an equipment.")
            return False

        if "all" not in item.role and character.role.lower() not in item.role:
            print(f"{item.role} does not belong to {character.name}, because the role doesn't match!")
            return False

        old_equipment = character._equip(slot, item)
        self.inventory[item] -= 1

        if self.inventory[item] <= 0:
            del self.inventory[item]

        if old_equipment:
            self.add_item(old_equipment)
        return True

    def unequip(self, character, item):
        if isinstance(item, Armor):
            equipment =character._unequip("armor")
        elif isinstance(item, Weapon):
            equipment =character._unequip("weapon")
        elif isinstance(item, Accessory):
            equipment =character._unequip("accessory")
        else:
            print(f"{item.name} is not an equipment.")
            return False

        if equipment is None:
            return False

        self.add_item(equipment)
        return True
