class WorlManager:
    def __init__(self, player):
        self.player = player
        self.player_x = 500
        self.player_y = 350
        self.player_speed = 5

    def move_player(self, dx, dy):
        self.player_x += dx
        self.player_y += dy