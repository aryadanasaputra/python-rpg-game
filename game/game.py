import pygame  # pyright: ignore[reportMissingImports]
from game.scenes.scene import SceneManager
from game.scenes.world.world_scene import WorldScene
from game.scenes.battle.battle_scene import BattleScene
from assets.fonts.font import Fonts
from systems.characters.player import Character
from systems.characters.monster import Monster
from systems.party import Party
from systems.skills.knight import WIND_SWING, RISING_SHIELD

class Game:
    def __init__(self, party, monsters):
        pygame.init()

        Fonts.initialize()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("RPG Game Python")

        self.clock = pygame.time.Clock()

        self.running = True

        self.party = party
        self.monsters = monsters

        self.scene_manager = SceneManager()
        self.world_scene = WorldScene(self.screen, self.party)
        self.battle_scene = BattleScene(self.screen, self.party, self.monsters)
        self.current_scene = self.battle_scene
        self.scene_manager.change_scene(self.world_scene)

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

            result = self.current_scene.handle_event(event)
            if result == "exit":
                self.running = False
            elif result == "world":
                self.scene_manager.change_scene(self.world_scene)
            elif result == "battle":
                self.scene_manager.change_scene(self.battle_scene)

    def update(self):
        self.scene_manager.current_scene.update()

    def draw(self):
        self.scene_manager.current_scene.draw()
        pygame.display.flip()