import pygame 
from src.engine.renderer import Renderer
from src.engine.game_object import GameObject
from src.engine.vector2 import Vector2

class RendererTest:
    def test_get_rect(self):
        img = pygame.Surface((25, 60))
        rend = Renderer(screen=pygame.Surface((100, 100)), img=img)
        go = GameObject(Vector2(70, 65), components=[rend])
        rend.update()

        right = pygame.Rect(0, 0, 25, 60).move(57.5, 35)
        actual = rend.get_rect()
        assert actual == right