import pygame # pyright: ignore[reportMissingImports]
from game.scenes.scene import Scene
from game.scenes.world.world_manager import WorldManager
from game.ui import Button, draw_confirmation_panel
from assets.fonts.font import Fonts

class WorldScene(Scene):
    def __init__(self, screen, player, monsters):
        self.screen = screen
        self.player = player
        self.selected_enemy = None

        self.world_state = "playing"
        self.world_manager = WorldManager(player, monsters)
        self.font = Fonts.medium
        self.confirm_yes_button = Button((330, 400, 150, 50), "Yes", Fonts.medium)
        self.confirm_no_button = Button((500, 400, 150, 50), "No", Fonts.medium)

    def handle_event(self, event):
        if self.world_state == "confirm_battle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.confirm_yes_button.is_clicked(event):
                    self.world_state = "playing"
                    return ("battle", self.selected_enemy.monster)
                if self.confirm_no_button.is_clicked(event):
                    self.world_state = "playing"
                    return "world"

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_GREATER):
                    self.world_state = "playing"
                    return ("battle", self.selected_enemy.monster)
                if event.key in (pygame.K_e, pygame.K_BACKSPACE):
                    self.world_state = "playing"
                    return "world"
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.selected_enemy = self.world_manager.get_colliding_enemy()
                if self.selected_enemy is not None:
                    self.world_state = "confirm_battle"

    def update(self):
        if self.world_state != "playing":
            return
        keys = pygame.key.get_pressed()
        self.world_manager.update(keys)

    def draw(self):
        self.screen.fill((50, 120, 50))

        pygame.draw.rect(
            self.screen,
            (50, 150, 255),
            self.world_manager.player_rect
        )
        for enemy in self.world_manager.enemies:
            if not enemy.monster.life:
                continue
            pygame.draw.rect(
                self.screen,
                (200, 50, 50),
                enemy.rect
            )
        text = Fonts.medium.render("WORLD", True, (255, 255, 255))

        self.screen.blit(text, (20, 20))

        if self.world_state == "confirm_battle":
            draw_confirmation_panel(self.screen, Fonts.big, "Do you want to fight this enemy?")
            self.confirm_yes_button.draw(self.screen)
            self.confirm_no_button.draw(self.screen)

        