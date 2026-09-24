import pygame # pyright: ignore[reportMissingImports]

class Fonts:
    big = None
    medium = None
    small = None

    @classmethod
    def initialize(cls):
        cls.big = pygame.font.Font("assets/fonts/eksternal/static/Oswald-Bold.ttf", 54)
        cls.medium = pygame.font.Font(None, 36)
        cls.small = pygame.font.Font(None, 24)