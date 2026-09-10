import pygame
from game.battle_scene import BattleScene
from systems.player import Character
from systems.monster import Monster

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("RPG Game Python")

        self.clock = pygame.time.Clock()

        self.running = True

        self.player = Character("Arya", "Knight", level=2)
        self.monster = Monster("Goblin", level=2)

        self.battle_scene = BattleScene(self.screen, self.player, self.monster)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.battle_scene.handle_event(event)

    def update(self):
        self.battle_scene.update()

    def draw(self):
        self.battle_scene.draw()
        pygame.display.flip()