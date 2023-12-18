from src.engine import game_object, renderer, vector2
import pygame
import utils

utils.game_pseudoinit()


def test_get_rect():
    go = game_object.GameObject()
    rend = renderer.Renderer()

    img = pygame.surface.Surface((60, 40))
    rend.init(go, img)
    go.init(None, scale=vector2.Vector2(1.2, 4),
            pos=vector2.Vector2(20, 70), components=[rend])

    right = pygame.rect.Rect(-16, -10, 72, 160)
    assert rend.get_rect() == right