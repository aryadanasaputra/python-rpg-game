import pygame # pyright: ignore[reportMissingImports]
from game.scenes.scene import Scene
from game.ui import Button, draw_bar, draw_battle_log, create_skill_buttons, create_item_buttons, draw_battle_result, draw_run
from game.scenes.battle.battle_manager import BattleManager

class BattleScene(Scene):
    def __init__(self, screen, party, monster):
        self.screen = screen
        self.party = party
        self.player = self.party.characters[0]
        self.monster = monster
        self.battle_manager = BattleManager(self.party, self.monster)

        # Set State Menu
        self.menu = "main"

        # Set font
        self.font_big = pygame.font.Font("assets/static/Oswald-Bold.ttf", 54)
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.attack_button = Button((100, 620, 150, 50), "Attack", self.font)
        self.skill_button = Button((270, 620, 150, 50), "Skill", self.font)
        self.item_button = Button((440, 620, 150, 50), "Item", self.font)
        self.run_button = Button((610, 620, 150, 50), "Run", self.font)

        self.back_button = Button((100, 620, 150, 50), "Back", self.font)
        # Generate Skill Button
        self.skill_buttons = create_skill_buttons(self.player.skills, self.font_small)
        self.item_buttons = {}

        self.continue_button = Button((400, 400, 200, 50), "Continue", self.font)
        self.run_yes_button = Button((330, 400, 150, 50), "Yes", self.font)
        self.run_no_button = Button((500, 400, 150, 50), "No", self.font)
        self.retry_button = Button((330, 400, 150, 50), "Retry", self.font)
        self.exit_button = Button((500, 400, 150, 50), "Exit", self.font)

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
        player_text = self.font.render(
            f"{self.player.name} (Lv.{self.player.level})", # Text yang akan muncul
            True,
            (255,255,255) # Warna
        )
        self.screen.blit(player_text, (100, 420))

        # Text Monster
        monster_text = self.font.render(
            f"{self.monster.name} (Lv.{self.monster.level})",
            True,
            (255,255,255)
        )
        self.screen.blit(monster_text, (750, 120))

        # HP Bar Player
        draw_bar(self.screen, self.player.health, self.player.max_health, 100, 570)
        hp_text = self.font_small.render(
            f"HP:",
            True,
            (255, 255, 255)
        )
        self.screen.blit(hp_text, (65, 567))
        hp_count_text = self.font_small.render(
            f"{self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(hp_count_text, (205, 567))
        
        # MP Bar Player
        draw_bar(self.screen, self.player.mana, self.player.max_mana, 100, 590, color=(91, 208, 243))
        mana_text = self.font_small.render(
            f"MP:",
            True,
            (255, 255, 255)
        )
        self.screen.blit(mana_text, (65, 587))
        mana_count_text = self.font_small.render(
            f"{self.player.mana}/{self.player.max_mana}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(mana_count_text, (205, 587))

        # HP Bar Monster
        draw_bar(self.screen, self.monster.health, self.monster.max_health, 750, 270)
        monster_hp_text = self.font.render(
            f"HP: {self.monster.health}/{self.monster.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(monster_hp_text, (750, 300))
        draw_battle_log(self.screen, self.font_small, self.battle_manager.battle_log)

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
            draw_run(self.screen, self.font_big)
            self.run_yes_button.draw(self.screen)
            self.run_no_button.draw(self.screen)

        turn_text = self.font.render(
            f"{self.battle_manager.turn.upper()} TURN",
            True,
            (255, 255, 255)
        )

        self.screen.blit(turn_text, (400, 50))


        if self.battle_manager.battle_state == "victory":
            draw_battle_result("VICTORY", self.screen, self.font_big)
            self.continue_button.draw(self.screen)
        elif self.battle_manager.battle_state == "defeat":
            draw_battle_result("DEFEAT", self.screen, self.font_big, color=(255, 0, 0))
            self.retry_button.draw(self.screen)
            self.exit_button.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.battle_manager.battle_state == "victory":
                if self.continue_button.is_clicked(event):
                    self.next_scene = "world"
                    return
            if self.battle_manager.battle_state == "defeat":
                if self.retry_button.is_clicked(event):
                    self.battle_manager.retry_battle()
                    self.menu = "main"
                    return
                if self.exit_button.is_clicked(event):
                    self.next_scene = "exit"
                    return
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
                    self.item_buttons = create_item_buttons(self.party.item_inventory, self.font_small)
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
            




