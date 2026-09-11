import pygame  # pyright: ignore[reportMissingImports]

# Method General Bar
def draw_bar(screen, current, maximum, x, y, width=100, height=10, color=(50, 200, 50)):
    ratio = current / maximum

    # Background bar
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (x, y, width, height)
    )

    # Current Bar
    pygame.draw.rect(
        screen,
        color,
        (x, y, width * ratio, height)
    )

# Battle Log
def draw_battle_log(screen, font, battle_log):
    pygame.draw.rect(
        screen,
        (128, 128, 128),
        (400, 450, 505, 155)
    )

    log_rect = pygame.Rect(402, 452, 500, 150)

    pygame.draw.rect(
        screen,
        (20, 20, 20),
        log_rect
    )

    title = font.render(
        "Battle Log",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (420, 460)
    )

    y = 495

    for message in battle_log[-4:]:
        text = font.render(
            message,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (420, y)
        )

        y += 30

class Button:
    def __init__(self, rect, text, font, background_color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

        self.background_color = background_color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return(
            event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
        )