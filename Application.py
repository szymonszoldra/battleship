import pygame
from Button import Button
from constants.colors import WHITE, BACKGROUND_COLOR
from constants.window import WIDTH, HEIGHT, FPS
from constants.fonts import FONT


class Application:
    def __init__(self):
        self._WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Battleship')

    def draw_window(self, text, btn):
        self._WINDOW.fill(BACKGROUND_COLOR)
        display_text = FONT.render(text, True, WHITE)
        self._WINDOW.blit(display_text,
                          (WIDTH // 2 - display_text.get_width() // 2, HEIGHT // 2 - display_text.get_height() // 2))
        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.draw_window('Hello World', btn)
        pygame.quit()
