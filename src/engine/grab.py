import pygame
from vector2 import Vector2


class Grabber:
    def __init__(self, screen, scene):
        self.screen = screen
        self.scene = scene

    def grab(self, screen, scene):
        mouse_pos = pygame.mouse.get_pos()

        