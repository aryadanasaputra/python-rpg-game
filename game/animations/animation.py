import pygame # pyright: ignore[reportMissingImports]

class GoldPopupAnimation:
    def __init__(self, screen):
        self.screen = screen
        self.gold_popup_amount = 0
        self.gold_popup_start = 0
        self.gold_popup_duration = 1500

    def show_gold_popup(self, amount):
        if amount <= 0:
            return
        self.gold_popup_amount = amount
        self.gold_popup_start = pygame.time.get_ticks()

    def draw(self, screen, font):
        elapsed_time = pygame.time.get_ticks() - self.gold_popup_start
        if self.gold_popup_amount > 0 and elapsed_time < self.gold_popup_duration:
            progress = elapsed_time / self.gold_popup_duration
            alpha = int(255 * (1 - progress))
            y = 100 - int(30 * progress)
            text = f"+{self.gold_popup_amount} Gold"
            text_surface = font.render(text, True, (255, 215, 0))
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(text_surface, text_rect)
