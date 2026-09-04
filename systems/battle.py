import os
import sys
import random
from systems.items.item import Item
from systems.equipments.equipment import Equipment

class Battle:
    def __init__(self, party, monsters):
        self.party = party
        self.monsters = monsters
        self.round = 1

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def alive_players(self):
        return [character for character in self.party.characters if character.life]

    def show_players(self, players=None):
        players = self.party.characters if players is None else players
        print("====== PARTY ======")
        for i, player in enumerate(players, start=1):
            status = "Alive" if player.life else "Dead"
            print(f"{i}. {player.name} HP: {player.health}/{player.max_health} [{status}]")
        print("===================")

    def choose_player(self, available_players=None):
        available_players = (
            self.alive_players()
            if available_players is None
            else available_players
        )
        if not available_players:
            return None

        while True:
            self.show_players(available_players)
            choice = input("Choose character (B to back): ")

            if choice.lower() == "b":
                return None

            if not choice.isdigit():
                print("Please enter a number!")
                continue

            index = int(choice) - 1
            if index < 0 or index >= len(available_players):
                print("Invalid character!")
                continue

            return available_players[index]

    def alive_monsters(self):
        return [monster for monster in self.monsters if monster.life] 

    def show_monsters(self):
        print("====== ENEMIES ======")
        for i, monster in enumerate(self.monsters, start=1):
            status = "Alive" if monster.life else "Dead"
            print(f"{i}. {monster.name} HP: {monster.health}/{monster.max_health} [{status}]")
        print("=====================")

    def choose_target(self):
        alive = self.alive_monsters()
        if not alive:
            return None

        while True:
            self.show_monsters()
            choice = input("Choose target (B to back): ")

            if choice.lower() ==  "b":
                return None

            if not choice.isdigit():
                print("Please enter a number!")
                continue

            index = int(choice) - 1
            if index < 0 or index >= len(self.monsters):
                print("Invalid target!")
                continue

            target = self.monsters[index]

            if not target.life:
                print(f"{target.name} is already dead.")
                continue

            return target

    def give_reward(self, monster):
        if monster.reward_given:
            return

        monster.reward_given = True
        exp_each = monster.experience_reward // len(self.party.characters)
        drop = monster.get_drop()

        for character in self.party.characters:
            character.gain_experience(exp_each)
        self.party.add_gold(monster.gold_reward)
        if drop:
            self.party.add_item(drop)

    def get_target(self, caster, target_type):

        if target_type == "self":
            return [caster]
        elif target_type == "all_allies":
            return self.alive_players()
        elif target_type == "ally":
            target = self.choose_player()
            if target:
                return [target]
        elif target_type == "all_enemies":
            return self.alive_monsters()
        elif target_type == "enemy":
            target = self.choose_target()
            if target is None:
                return []
            return [target]

        return []

    def get_effect_target(self, caster, skill):
        effect_target  = skill.effect_target

        if effect_target == "self":
            return [caster]
        elif effect_target == "all_allies":
            return self.alive_players()
        elif effect_target == "ally":
            target = self.choose_player()
            if target:
                return [target]
        elif effect_target == "all_enemies":
            return self.alive_monsters()
        elif effect_target == "enemy":
            target = self.choose_target()
            if target is None:
                return []
            return [target]

        return []

    def player_turn(self, player_character):
        while True:
            print("\n======================")
            print("     PLAYER TURN")
            print("======================")
            print(f"Nama    : {player_character.name} ({player_character.role})\n"
                  f"HP      : {player_character.health}/{player_character.max_health}\n"
                  f"MP      : {player_character.mana}/{player_character.max_mana}\n"
                  f"Level   : {player_character.level}\n"
                  f"EXP     : {player_character.experience}/{player_character.experience_limit}\n"
                  f"Attack  : {player_character.attack}\n"
                  f"Defense : {player_character.defense}")
            print("======================")

            print("Choose action:")
            print("1. Attack")
            print("2. Skill")
            print("3. Inventory")
            print("4. Status")
            print("5. Run")
            print("6. Clear Screen")
            print("\n0. Exit Game")

            choice = input("Choose action: ")

            if choice == "1":
                target = self.choose_target()
                if target is None:
                    continue
                player_character.attack_target(target)
                if target in self.monsters and not target.life:
                    self.give_reward(target)
                return "used"

            elif choice == "2":
                self.clear_screen()
                if not player_character.skills:
                    print("No skills learned yet!")
                    continue
                
                print("======== PLAYER SKILL ========")
                for i, skill_list in enumerate(player_character.skills, start=1):
                    print(f"{i}. {skill_list.name} (MP: {skill_list.mana_cost})")
                print("==============================")
                print(f"Current {player_character.name} MP: {player_character.mana}/{player_character.max_mana}\n")
                skill_choice = input("Choose skill you want to use (B to back): ")
                if skill_choice.lower() == "b":
                    self.clear_screen()
                    continue
                elif not skill_choice.isdigit():
                    print("Please enter a number")
                    continue
                
                index = int(skill_choice) - 1
                if index < 0 or index >= len(player_character.skills):
                    print("Invalid skill choice")
                    continue
                selected_skill = player_character.skills[index]

                targets = self.get_target(player_character, selected_skill.target_type)

                if not targets:
                    print("No valid targets for this skill.")
                    continue

                effect_targets = []
                if selected_skill.effect is not None:
                    if selected_skill.effect_target == selected_skill.target_type:
                        effect_targets = targets
                    else:
                        effect_targets = self.get_target(player_character, selected_skill.effect_target)

                success = player_character.use_skill(selected_skill, targets, effect_targets)
                if success:
                    for target in targets:
                        if target in self.monsters and not target.life:
                            self.give_reward(target)
                    return "used"

            elif choice == "3":
                self.clear_screen()
                if not self.party.inventory:
                    print("No item")

                print("======== PLAYER INVENTORY ========")
                print("Items:")
                for i, (item, quantity) in enumerate(self.party.inventory.items(), start=1):
                    if isinstance(item, Item):
                        print(f"{i}. {item.name:<25} x{quantity}")
                print("\nEquipment:")
                for i, (item, quantity) in enumerate(self.party.inventory.items(), start=1):
                    if isinstance(item, Equipment):
                        print(f"{i}. {item.name:<25} x{quantity}")
                print("\nCurrent Equipment:")
                for slot, item in player_character.equipment.items():
                    name = item.name if item else "None"
                    print(f"{slot.title():<10}: {name}")
                print("==================================\n")
                
                item_choice = input("Choose an item/equipment (B to back): ")
                if item_choice.lower() == "b":
                    self.clear_screen()
                    continue
                elif not item_choice.isdigit():
                    print("Please enter a number")
                    continue

                index = int(item_choice) - 1
                items = list(self.party.inventory.keys())
                if 0 <= index < len(items):
                    selected_item = items[index]

                    if isinstance(selected_item, Equipment):
                        success = self.party.equip(player_character, selected_item)
                    else:
                        targets = self.get_target(player_character, selected_item.target_type)
                        if not targets:
                            print(f"No valid target for using item.")
                            continue
                        success = self.party.use_item(selected_item, targets)
                    if success:
                        return "used"
                else:
                    print("Invalid item choice")
                    
            elif choice == "4":
                self.clear_screen()
                player_character.info()
                self.show_players()
                for monster in self.monsters:
                    monster.info()
                continue

            elif choice == "5":
                if random.random()>0.5:
                    print(f"{player_character.name} ran away!")
                    return "run"
                else:
                    self.clear_screen()
                    print(f"The monster block your way!")
                    continue

            elif choice == "6" or choice.lower() in ("cls", "clear"):
                self.clear_screen()

            elif choice == "0":
                return "quit"
            
            else:
                print("Invalid choice")
                continue

    def monster_turn(self):
        print("\n====================")
        print("    MONSTER TURN")
        print("====================")

        for monster in self.alive_monsters():
            players = self.alive_players()
            if not players:
                break
            monster.attack(random.choice(players))

    def battle(self):
        while self.alive_players() and self.alive_monsters():
            print(f"ROUND = {self.round}")

            available_players = self.alive_players()
            while available_players:
                if not self.alive_monsters():
                    break

                player = self.choose_player(available_players)
                if player is None:
                    return "run"

                result = self.player_turn(player)
                available_players.remove(player)
                if result == "run":
                    return "run"
                if result == "quit":
                    return "quit"

            if not self.alive_monsters():
                break

            self.monster_turn()
            for player in self.alive_players():
                player.process_effect()
            for monster in self.monsters:
                monster.process_effect()
            self.round += 1

        if not self.alive_players():
            print("\nAll players have been defeated!")
            return "defeat"
        elif not self.alive_monsters():
            print("\nYou defeated all monsters!")
            total_exp = 0
            total_gold = 0
            for monster in self.monsters:
                total_exp += monster.experience_reward
                total_gold += monster.gold_reward
            print(f"Total EXP  : {total_exp}")
            print(f"Total Gold : {total_gold}")
            return "victory"
        else:
            self.clear_screen()
            print("\nYou escaped!")
            return "run"