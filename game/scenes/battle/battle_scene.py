import pygame # pyright: ignore[reportMissingImports]
from game.scenes.scene import Scene
from game.ui import Button, draw_bar, draw_battle_log, create_skill_buttons, create_item_buttons, draw_battle_result, draw_run
from game.scenes.battle.battle_manager import BattleManager
from assets.fonts.font import Fonts

class BattleScene(Scene):
    def __init__(self, screen, party, monster):
        self.screen = screen
        self.party = party
        self.player = self.party.characters[0]
        self.monster = monster
        self.battle_manager = BattleManager(self.party, self.monster)

        # Set State Menu
        self.menu = "main"

        self.attack_button = Button((100, 620, 150, 50), "Attack", Fonts.medium)
        self.skill_button = Button((270, 620, 150, 50), "Skill", Fonts.medium)
        self.item_button = Button((440, 620, 150, 50), "Item", Fonts.medium)
        self.run_button = Button((610, 620, 150, 50), "Run", Fonts.medium)

        self.back_button = Button((100, 620, 150, 50), "Back", Fonts.medium)
        # Generate Skill Button
        self.skill_buttons = create_skill_buttons(self.player.skills, Fonts.small)
        self.item_buttons = {}

        self.continue_button = Button((400, 400, 200, 50), "Continue", Fonts.medium)
        self.run_yes_button = Button((330, 400, 150, 50), "Yes", Fonts.medium)
        self.run_no_button = Button((500, 400, 150, 50), "No", Fonts.medium)
        self.retry_button = Button((330, 400, 150, 50), "Retry", Fonts.medium)
        self.exit_button = Button((500, 400, 150, 50), "Exit", Fonts.medium)

        self.next_scene = None


    def update(self):
        self.battle_manager.update()

    def draw(self):
        self.screen.fill((30, 30, 30))
        # Player
        pygame.draw.rect(
            self.screen,
            (50, 150, 255), # Warna
            (100, 450, 50, 100) # Posisi & Ukuran
            # (posisi X, posisi Y, Lebar, Tinggi)
        )

        # Monster
        pygame.draw.rect(
            self.screen,
            (200, 50, 50),
            (750, 150, 100, 100)
        )

        # Text Player
        player_text = Fonts.medium.render(
            f"{self.player.name} (Lv.{self.player.level})", # Text yang akan muncul
            True,
            (255,255,255) # Warna
        )
        self.screen.blit(player_text, (100, 420))

        # Text Monster
        monster_text = Fonts.medium.render(
            f"{self.monster.name} (Lv.{self.monster.level})",
            True,
            (255,255,255)
        )
        self.screen.blit(monster_text, (750, 120))

        # HP Bar Player
        draw_bar(self.screen, self.player.health, self.player.max_health, 100, 570)
        hp_text = Fonts.small.render(
            f"HP:",
            True,
            (255, 255, 255)
        )
        self.screen.blit(hp_text, (65, 567))
        hp_count_text = Fonts.small.render(
            f"{self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(hp_count_text, (205, 567))
        
        # MP Bar Player
        draw_bar(self.screen, self.player.mana, self.player.max_mana, 100, 590, color=(91, 208, 243))
        mana_text = Fonts.small.render(
            f"MP:",
            True,
            (255, 255, 255)
        )
        self.screen.blit(mana_text, (65, 587))
        mana_count_text = Fonts.small.render(
            f"{self.player.mana}/{self.player.max_mana}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(mana_count_text, (205, 587))

        # HP Bar Monster
        draw_bar(self.screen, self.monster.health, self.monster.max_health, 750, 270)
        monster_hp_text = Fonts.medium.render(
            f"HP: {self.monster.health}/{self.monster.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(monster_hp_text, (750, 300))
        draw_battle_log(self.screen, Fonts.small, self.battle_manager.battle_log)

        if self.menu == "main":
            self.attack_button.draw(self.screen)
            self.skill_button.draw(self.screen)
            self.item_button.draw(self.screen)
            self.run_button.draw(self.screen)
        elif self.menu == "skills":
            for button in self.skill_buttons.values():
                button.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.menu == "items":
            for button in self.item_buttons.values():
                button.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.menu == "run":
            draw_run(self.screen, Fonts.big)
            self.run_yes_button.draw(self.screen)
            self.run_no_button.draw(self.screen)

        turn_text = Fonts.medium.render(
            f"{self.battle_manager.turn.upper()} TURN",
            True,
            (255, 255, 255)
        )

        self.screen.blit(turn_text, (400, 50))


        if self.battle_manager.battle_state == "victory":
            draw_battle_result("VICTORY", self.screen, Fonts.big)
            self.continue_button.draw(self.screen)
        elif self.battle_manager.battle_state == "defeat":
            draw_battle_result("DEFEAT", self.screen, Fonts.big, color=(255, 0, 0))
            self.retry_button.draw(self.screen)
            self.exit_button.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.battle_manager.battle_state == "victory":
                if self.continue_button.is_clicked(event):
                    self.next_scene = "world"
                    return self.next_scene
            if self.battle_manager.battle_state == "defeat":
                if self.retry_button.is_clicked(event):
                    self.battle_manager.retry_battle()
                    self.menu = "main"
                    return
                if self.exit_button.is_clicked(event):
                    self.next_scene = "exit"
                    return self.next_scene
        if self.battle_manager.battle_state != "playing":
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu == "main":
                if self.attack_button.is_clicked(event):
                    if self.battle_manager.turn == "player":
                        result = self.battle_manager.player_attack()
                        if result is None:
                            return
                        return
                if self.skill_button.is_clicked(event):
                    self.menu = "skills"
                    return
                if self.item_button.is_clicked(event):
                    self.menu = "items"
                    self.item_buttons = create_item_buttons(self.party.item_inventory, Fonts.small)
                    return
                if self.run_button.is_clicked(event):
                    self.menu = "run"
                    return
            if self.menu == "skills":
                for skill, button in self.skill_buttons.items():
                    if button.is_clicked(event):
                        if self.battle_manager.turn != "player":
                            return
                        success = self.battle_manager.use_skill(skill)
                        if not success:
                            return
                        self.menu = "main"
                        return
                if self.back_button.is_clicked(event):
                    self.menu = "main"
                    return
            if self.menu == "items":
                for item, button in self.item_buttons.items():
                    if button.is_clicked(event):
                        if self.battle_manager.turn == "player":
                            self.battle_manager.use_item(item)
                        self.menu = "main"
                        return
                if self.back_button.is_clicked(event):
                    self.menu = "main"
                    return
            if self.menu == "run":
                if self.run_yes_button.is_clicked(event):
                    self.next_scene = "exit"
                    return
                if self.run_no_button.is_clicked(event):
                    self.menu = "main"
                    return
            




