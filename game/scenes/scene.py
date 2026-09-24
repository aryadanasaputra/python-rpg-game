class SceneManager:
    def __init__(self):
        self.current_scene = None

    def change_scene(self, scene):
        self.current_scene = scene

class Scene:
    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass