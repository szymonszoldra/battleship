import pygame
import os

pygame.font.init()

FONT_PATH = os.path.join(os.getcwd(), 'assets/CascadiaCode.ttf')
FONT = pygame.font.Font(FONT_PATH, 40)
