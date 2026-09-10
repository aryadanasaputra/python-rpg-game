import pygame

class BattleScene:
    def __init__(self, screen, player, monster):
        self.screen = screen
        self.player = player
        self.monster = monster

        self.attack_button = pygame.Rect(100, 620, 150, 50)
        # Set font
        self.font = pygame.font.Font(None, 36)

    def update(self):
        pass

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
            self.player.name, # Text yang akan muncul
            True,
            (255,255,255) # Warna
        )
        self.screen.blit(player_text, (100, 420))

        # Text Monster
        monster_text = self.font.render(
            self.monster.name,
            True,
            (255,255,255)
        )
        self.screen.blit(monster_text, (750, 120))

        self.draw_health_bar(
            self.player,
            100,
            570
        )
        self.draw_health_bar(
            self.monster,
            750,
            270
        )

        hp_text = self.font.render(
            f"HP: {self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(hp_text, (100, 600))

        monster_hp_text = self.font.render(
            f"HP: {self.monster.health}/{self.monster.max_health}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(monster_hp_text, (750, 300))

        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            self.attack_button
        )

        attack_text = self.font.render(
            "Attack",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            attack_text,
            (125, 630)
        )

    def draw_health_bar(self, character, x, y, width=100, height=10):
        health_ratio = character.health / character.max_health

        # Background bar
        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            (x, y, width, height)
        )

        # Current HP
        pygame.draw.rect(
            self.screen,
            (50, 200, 50),
            (x, y, width * health_ratio, height)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.attack_button.collidepoint(event.pos):
                print("Attack ditekan!")