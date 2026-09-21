import pygame  # pyright: ignore[reportMissingImports]
from game.battle.battle_scene import BattleScene
from systems.characters.player import Character
from systems.characters.monster import Monster
from systems.party import Party
from systems.skills.knight import WIND_SWING, RISING_SHIELD

class Game:
    def __init__(self, party, monsters):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("RPG Game Python")

        self.clock = pygame.time.Clock()

        self.running = True

        self.party = party
        self.monsters = monsters

        self.battle_scene = BattleScene(self.screen, self.party, self.monsters)
        self.current_scene = self.battle_scene

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
                return

            self.current_scene.handle_event(event)
            if self.current_scene.next_scene == "exit":
                self.running = False
                return

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.current_scene.draw()
        pygame.display.flip()