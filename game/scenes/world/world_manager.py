import pygame # pyright: ignore[reportMissingImports]

class WorldManager:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player_speed = 5
        self.player_rect = pygame.Rect(500, 350, 50, 50)
        self.enemy_rect = pygame.Rect(700, 300, 50, 50)

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

    def check_enemy_collision(self):
        return self.enemy.life and self.player_rect.colliderect(self.enemy_rect)

    def get_colliding_enemy(self):
        if not self.enemy.life:
            return None
        if self.player_rect.colliderect(self.enemy_rect):
            return self.enemy
        return None