class BattleManager:
    def __init__(self, party):
        self.party = party
        self.player = party.characters[0]
        self.monster = None
        self.battle_log = []

        self.battle_state = "playing"
        self.turn = "player"

    def update(self):
        if self.turn == "monster":
            self.monster_turn()

    def start_battle(self, monster):
        self.monster = monster
        self.battle_state = "playing"
        self.turn = "player"
        self.battle_log.clear()

    def check_battle_result(self):
        if self.battle_state != "playing":
            return True
        
        if not self.monster.life:
            self.battle_state = "victory"
            messages = self.give_reward()
            for message in messages:
                self.add_log(message)
            return True

        if not self.player.life:
            self.battle_state = "defeat"
            return True
        return False

    def monster_turn(self):
        if self.check_battle_result():
            return

        result = self.monster.attack_target(self.player)

        if result is None:
            self.check_battle_result()
            return

        if not result.get("success", False):
            for message in result.get("messages", []):
                self.add_log(message)
            return

        for message in result.get("messages", []):
            self.add_log(message)

        combat_result = result.get("combat", {})
        status = combat_result.get("status")
        if status is not None:
            self.add_log(status)

        if self.check_battle_result():
            return

        self.end_monster_turn()  

    def end_player_turn(self):
        messages = self.player.process_effect()
        for message in messages:
            self.add_log(message)
        if not self.monster.life:
            return
        self.turn = "monster"

    def end_monster_turn(self):
        messages = self.monster.process_effect()
        for message in messages:
            self.add_log(message)
        if not self.player.life:
            return
        self.turn = "player"

    def use_item(self, item):
        targets = [self.player]
        result = self.party.use_item(item, targets)
        if not result["success"]:
            for message in result["messages"]:
                self.add_log(message)
            return False
        for message in result["messages"]:
            self.add_log(message)
        if self.check_battle_result():
            return True
        self.end_player_turn()
        return True

    def player_attack(self):
        result = self.player.attack_target(self.monster)
        if not result.get("success", False):
            for message in result.get("messages", []):
                self.add_log(message)
            return result

        for message in result.get("messages", []):
            self.add_log(message)

        combat_result = result.get("combat", {})
        status = combat_result.get("status")
        if status is not None:
            self.add_log(status)

        if self.check_battle_result():
            return result
        self.end_player_turn()
        return result

    def use_skill(self, skill):
        targets = []
        if skill.damage > 0:
            targets = [self.monster]
        effect_targets = []
        if skill.effect is not None:
            if skill.effect_target == "self":
                effect_targets = [self.player]
            elif skill.effect_target == "enemy":
                effect_targets = [self.monster]
        
        result = self.player.use_skill(skill, targets, effect_targets)
        for message in result.get("messages", []):
            self.add_log(message)
        if not result.get("success", False):
            return False
        if self.check_battle_result():
            return True
        self.end_player_turn()
        return True

    def give_reward(self):
        if self.monster.reward_given:
            return []

        self.monster.reward_given = True
        messages = []
        exp_each = self.monster.experience_reward // len(self.party.characters)
        for character in self.party.characters:
            messages.extend(character.gain_experience(exp_each))

        messages.append(self.party.add_gold(self.monster.gold_reward))

        drop_item = self.monster.get_drop()
        if drop_item is not None:
            item_message = self.party.add_item(drop_item)
            if isinstance(item_message, str):
                messages.append(item_message)
            else:
                messages.append(f"Could not add {drop_item.name} to the party inventory.")

        return messages

    def retry_battle(self):
        self.player.health = self.player.max_health
        self.player.mana = self.player.max_mana
        self.player.effects.clear()
        self.player.life = True

        self.monster.health = self.monster.max_health
        self.monster.effects.clear()
        self.monster.life = True

        self.battle_state = "playing"
        self.turn = "player"
        self.battle_log.clear()

    def add_log(self, message):
        self.battle_log.append(message)