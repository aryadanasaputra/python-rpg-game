import pygame # pyright: ignore[reportMissingImports]
from game.scenes.scene import Scene
from game.scenes.world.world_manager import WorlManager
from game.ui import Button
from assets.fonts.font import Fonts

class WorldScene(Scene):
    def __init__(self, screen, player):
        self.screen = screen
        self.palyer = player

        self.world_manager = WorlManager(player)
        self.font = Fonts.medium

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.k_w:
                self.world_manager.move_player(0,  -5)
            elif event.key == pygame.k_s:
                self.world_manager.move_player(0,  5)
            elif event.key == pygame.k_a:
                self.world_manager.move_player(-5,  0)
            elif event.key == pygame.k_d:
                self.world_manager.move_player(5,  0)

    def update(self):
        pass

    def draw(self):
        self.screen.fill((50, 120, 50))

        pygame.draw.rect(
            self.screen,
            (50, 150, 255),
            (self.world_manager.player_x, self.world_manager.player_y, 50, 50)
        )
        text = Fonts.medium.render("WORLD", True, (255, 255, 255))

        self.screen.blit(text, (20, 20))

        