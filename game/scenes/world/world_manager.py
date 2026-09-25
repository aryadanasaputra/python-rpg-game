import pygame # pyright: ignore[reportMissingImports]

class WorldManager:
    def __init__(self, player):
        self.player = player
        self.player_x = 500
        self.player_y = 350
        self.player_speed = 5
        self.player_rect = pygame.Rect(500, 350, 50, 50)
        self.enemy_rect = pygame.Rect(700, 300, 50, 50)

    def update(self, keys):
        if keys[pygame.K_w]:
            self.player_rect.y -= self.player_speed
            print("Player bergerak ke atas")

        if keys[pygame.K_s]:
            self.player_rect.y += self.player_speed

        if keys[pygame.K_a]:
            self.player_rect.x -= self.player_speed

        if keys[pygame.K_d]:
            self.player_rect.x += self.player_speed

        self.player_rect.x = max(0, min(self.player_rect.x, 950))
        self.player_rect.y = max(0, min(self.player_rect.y, 650))

    def check_enemy_collision(self):
        return self.player_rect.colliderect(self.enemy_rect)