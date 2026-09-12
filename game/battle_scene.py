import pygame # pyright: ignore[reportMissingImports]
from game.ui import Button, draw_bar, draw_battle_log
from systems.skills.knight import WIND_SWING

class BattleScene:
    def __init__(self, screen, player, monster):
        self.screen = screen
        self.player = player
        self.monster = monster

        # Set State Menu
        self.menu = "main"

        # Set font
        self.font_small = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 36)

        self.attack_button = Button((100, 620, 150, 50), "Attack", self.font)
        self.skill_button = Button((270, 620, 150, 50), "Skill", self.font)
        self.item_button = Button((440, 620, 150, 50), "Item", self.font)
        self.run_button = Button((610, 620, 150, 50), "Run", self.font)

        self.wind_swing_button = Button((100, 620, 150, 50), "Wind Swing", self.font)
        self.back_button = Button((270, 620, 150, 50), "Back", self.font)

        self.turn = "player"
        player.learn_skill(WIND_SWING)

        self.battle_log = []

    def update(self):
        if self.turn =="monster":
            self.monster_turn()

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

        if self.menu == "main":
            self.attack_button.draw(self.screen)
            self.skill_button.draw(self.screen)
            self.item_button.draw(self.screen)
            self.run_button.draw(self.screen)
        elif self.menu == "skills":
            self.wind_swing_button.draw(self.screen)
            self.back_button.draw(self.screen)

        turn_text = self.font.render(
            f"{self.turn.upper()} TURN",
            True,
            (255, 255, 255)
        )

        self.screen.blit(turn_text, (400, 50))

        draw_battle_log(self.screen, self.font_small, self.battle_log)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu == "main":
                if self.attack_button.is_clicked(event):
                    if self.turn == "player":
                        self.player.attack_target(self.monster)
                        self.add_log(f"{self.player.name} attacks {self.monster.name}!")
                        if not self.monster.life:
                            return
                        self.turn = "monster"
                if self.skill_button.is_clicked(event):
                    self.menu = "skills"
                    return
            if self.menu == "skills":
                if self.wind_swing_button.is_clicked(event):
                    if self.turn == "player":
                        self.player.use_skill(WIND_SWING, [self.monster], "enemy")
                        self.add_log(f"{self.player.name} attacks Wind Swing!")
                        if not self.monster.life:
                            return
                        self.turn = "monster"
                if self.back_button.is_clicked(event):
                    self.menu = "main"
                    return
                
                    
    def monster_turn(self):
        self.monster.attack(self.player)
        self.add_log(f"{self.monster.name} attacks {self.player.name}!")
        self.turn = "player"

    def add_log(self, message):
        self.battle_log.append(message)

