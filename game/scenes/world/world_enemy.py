import pygame # pyright: ignore[reportMissingImports]

class WorldEnemy:
    def __init__(self, monster, x, y):
        self.monster = monster
        self.rect = pygame.Rect(x, y, 50, 50)