import unittest
import pygame 
from engine.renderer import Renderer
from engine.game_object import GameObject
from engine.vector2 import Vector2

class RendererTest(unittest.TestCase):
    def test_get_rect(self):
        img = pygame.Surface((25, 60))
        rend = Renderer(screen=pygame.Surface((100, 100)), img=img)
        go = GameObject(Vector2(70, 65), components=[rend])
        rend.update()

        right = pygame.Rect(0, 0, 25, 60).move(57.5, 35)
        actual = rend.get_rect()
        self.assertEqual(actual, right)