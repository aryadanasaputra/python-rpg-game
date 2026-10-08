import pygame # pyright: ignore[reportMissingImports]
import random
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
        self.obstacles = [
            pygame.Rect(200, 150, 200, 50),
            pygame.Rect(600, 300, 50, 200),
            pygame.Rect(350, 500, 250, 50),
        ]
        self.quantity_decorations = 15
        self.decorations = self.create_decorations()

    def update(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_w]  or keys[pygame.K_UP]:
            dy -= self.player_speed

        if keys[pygame.K_s]  or keys[pygame.K_DOWN]:
            dy += self.player_speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player_speed

        if keys[pygame.K_d]  or keys[pygame.K_RIGHT]:
            dx += self.player_speed

        self.move_player(dx, dy, self.get_collision_checks())

        self.player_rect.x = max(0, min(self.player_rect.x, 950))
        self.player_rect.y = max(0, min(self.player_rect.y, 650))

    def get_colliding_enemy(self):
        for enemy in self.enemies:
            if not enemy.monster.life:
                continue
            if self.player_rect.colliderect(enemy.rect):
                return enemy
        return None

    def is_colliding_obstacle(self):
        for obstacle in self.obstacles:
            if self.player_rect.colliderect(obstacle):
                return True
        return False

    # New method to check collision with decorations (not in_use yet)
    def is_colliding_decoration(self):
        for decoration in self.decorations:
            if self.player_rect.colliderect(decoration):
                return True
        return False

    def is_colliding(self, check_collisions):
        for check_collision in check_collisions:
            if check_collision:
                return True
        return False

    def get_collision_checks(self):
        return [self.is_colliding_obstacle(), self.is_colliding_decoration()]

    def move_player(self, dx, dy, check_collisions):
        self.player_rect.x += dx
        check_collisions[:] = self.get_collision_checks()
        if self.is_colliding(check_collisions):
            self.player_rect.x -= dx
        self.player_rect.y += dy
        check_collisions[:] = self.get_collision_checks()
        if self.is_colliding(check_collisions):
            self.player_rect.y -= dy

    def create_decorations(self):
        decorations = []

        for _ in range(self.quantity_decorations):
            while True:
                decoration = pygame.Rect(random.randint(0, 960), random.randint(0, 660), 40, 40)
                if self.is_valid_decoration_possition(decoration, decorations):
                    decorations.append(decoration)
                    break

        return decorations

    def is_valid_decoration_possition(self, decoration, existing_decorations):
        if decoration.colliderect(self.player_rect):
            return False
        for obstacle in self.obstacles:
            if decoration.colliderect(obstacle):
                return False
        for enemy in self.enemies:
            if decoration.colliderect(enemy.rect):
                return False
        for other_decoration in existing_decorations:
            if decoration.colliderect(other_decoration.inflate(-20, -20)):
                return False
        return True