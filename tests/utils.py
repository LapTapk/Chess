import pygame
from src.engine import game


def game_pseudoinit():
    if game.is_init:
        return

    pygame.display.set_mode = lambda x: pygame.surface.Surface(x)
    game.init((1280, 720), 60, 'game_data.json')
