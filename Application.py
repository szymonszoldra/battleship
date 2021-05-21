import pygame

pygame.font.init()

WIDTH = 900
HEIGHT = 500
FPS = 60

# colors
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (50, 50, 50)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

FONT = pygame.font.SysFont('comicsans', 40)


class Application:
    def __init__(self):
        pass

    @staticmethod
    def draw_window(text):
        WINDOW.fill(BACKGROUND_COLOR)

        display_text = FONT.render(text, True, WHITE)
        WINDOW.blit(display_text,
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

            self.draw_window('Hello World')
        pygame.quit()
