class BattleManager:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.battle_log = []

        self.battle_state = "playing"
        self.turn = "player"

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
        result = self.monster.attack(self.player)
        if result is None:
            return
        self.add_log(result["message"])
        if result.get("status") is not None:
            self.add_log(result["status"])
        if self.check_battle_result():
            return
        self.end_monster_turn()    

    def end_player_turn(self):
        self.player.process_effect()
        if not self.monster.life:
            return
        self.turn = "monster"

    def end_monster_turn(self):
        self.monster.process_effect()
        if not self.player.life:
            return
        self.turn = "player"

    def player_attack(self):
        result = self.player.attack_target(self.monster)
        if result is None:
            return
        if self.check_battle_result():
            return
        self.add_log(f"{self.player.name} rolls {result['roll']}.")
        self.add_log(result["message"])
        if result.get("status") is not None:
            self.add_log(result["status"])
        self.end_player_turn()

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
        
        success = self.player.use_skill(skill, targets, effect_targets)
        if not success:
            return False
        self.add_log(f"{self.player.name} uses {skill.name}!")
        if self.check_battle_result():
            return True
        self.end_player_turn()
        return True

    def give_reward(self):
        reward = self.monster.experience_reward
        return self.player.gain_experience(reward)

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