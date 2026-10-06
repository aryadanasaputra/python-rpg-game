import pygame # pyright: ignore[reportMissingImports]
from game.scenes.world.world_enemy import WorldEnemy

class WorldManager:
    def __init__(self, player, enemy_data):
        self.player = player
        self.player_speed = 5
        self.player_rect = pygame.Rect(500, 350, 50, 50)
        self.enemies = [
                WorldEnemy(enemy["monster"], enemy["x"], enemy["y"])
                for enemy in enemy_data
            ]

    def update(self, keys):
        if keys[pygame.K_w]  or keys[pygame.K_UP]:
            self.player_rect.y -= self.player_speed

        if keys[pygame.K_s]  or keys[pygame.K_DOWN]:
            self.player_rect.y += self.player_speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed

        if keys[pygame.K_d]  or keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed

        self.player_rect.x = max(0, min(self.player_rect.x, 950))
        self.player_rect.y = max(0, min(self.player_rect.y, 650))

    def get_colliding_enemy(self):
        for enemy in self.enemies:
            if not enemy.monster.life:
                continue
            if self.player_rect.colliderect(enemy.rect):
                return enemy
        return None