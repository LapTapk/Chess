import pygame
from src.engine import game


def game_pseudoinit(scr_size=(1280, 720), fps=60):
    pygame.display.set_mode = lambda x: pygame.surface.Surface(x)
    game.init(scr_size, fps, 'game_data.json')
