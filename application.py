import pygame
from constants.colors import WHITE, BACKGROUND_COLOR, BUTTON_COLOR
from constants.window import WIDTH, HEIGHT, FPS
from constants.fonts import FONT
from constants.difficulty import DEFAULT

from components.button import Button

from screens.game import Game
from screens.options import Options


class Application:
    def __init__(self) -> None:
        self._WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Battleship')

        self._difficulty = DEFAULT
        self._btn_options = Button(BUTTON_COLOR, WIDTH // 2, HEIGHT // 3 * 2, 200, 80, 'Options')
        self._btn_game = Button(BUTTON_COLOR, WIDTH // 2, HEIGHT // 3, 200, 80, 'Start')

    def draw_window(self, text: str) -> None:
        self._WINDOW.fill(BACKGROUND_COLOR)
        display_text = FONT.render(text, True, WHITE)
        self._WINDOW.blit(display_text,
                          (WIDTH // 2 - display_text.get_width() // 2, HEIGHT // 2 - display_text.get_height() // 2))

        self._btn_options.draw(self._WINDOW, font_size=30)
        self._btn_game.draw(self._WINDOW, font_size=30)
        pygame.display.update()

    def set_difficulty(self, difficulty: str) -> None:
        self._difficulty = difficulty

    def change_options(self) -> None:
        options = Options(self._WINDOW)
        options.set_options(self.set_difficulty)

    def play_game(self) -> None:
        should_start_new_game = True
        while should_start_new_game:
            game = Game(self._WINDOW, self._difficulty)
            _, should_start_new_game = game.start()

    def run(self) -> None:
        run = True
        clock = pygame.time.Clock()
        click = False
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()

            if self._btn_options.is_mouse_over(mouse_coords) and click:
                self.change_options()

            if self._btn_game.is_mouse_over(mouse_coords) and click:
                self.play_game()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            self.draw_window(f'Current difficulty {self._difficulty}')
        pygame.quit()
