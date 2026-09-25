import pygame # pyright: ignore[reportMissingImports]
from game.scenes.scene import Scene
from game.scenes.world.world_manager import WorldManager
from game.ui import Button
from assets.fonts.font import Fonts

class WorldScene(Scene):
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.world_manager = WorldManager(player)
        self.font = Fonts.medium

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.world_manager.check_enemy_collision():
                    print("Player wants to fight!")
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         self.world_manager.move_player(0, -5)
        #     elif event.key == pygame.K_s:
        #         self.world_manager.move_player(0, 5)
        #     elif event.key == pygame.K_a:
        #         self.world_manager.move_player(-5, 0)
        #     elif event.key == pygame.K_d:
        #         self.world_manager.move_player(5, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        self.world_manager.update(keys)

    def draw(self):
        self.screen.fill((50, 120, 50))

        pygame.draw.rect(
            self.screen,
            (50, 150, 255),
            self.world_manager.player_rect
        )
        pygame.draw.rect(
            self.screen,
            (200, 50, 50),
            self.world_manager.enemy_rect
        )
        text = Fonts.medium.render("WORLD", True, (255, 255, 255))

        self.screen.blit(text, (20, 20))

        