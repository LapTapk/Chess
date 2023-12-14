import utils
import pygame
import unittest.mock as mock
from src.engine import game_object, input_box, game, vector2

utils.game_pseudoinit()

def test_activation():
    go = game_object.GameObject()
    ib = input_box.InputBox()

    ib.init(go, 32, 'INVITATION')
    go.init(None, pos = vector2.Vector2(20, 60), components=[ib])
    ib.show_text()

    event = mock.Mock()
    event.type = pygame.MOUSEBUTTONDOWN
    game.events = [event]

    ib_rect = ib.surface.get_rect()
    m_pos = go.position + vector2.Vector2(ib_rect.x + 1, ib_rect.y + 1)
    m_pos = m_pos.to_tuple()
    pygame.mouse.get_pos = lambda: m_pos

    ib.update()
    assert ib.active == True

def test_text_input():
    go = game_object.GameObject()
    ib = input_box.InputBox()

    ib.init(go, 32, 'INVITATION')
    go.init(None, pos = vector2.Vector2(20, 60), components=[ib])
    ib.active = True

    event = mock.Mock()
    event.type = pygame.KEYDOWN
    event.unicode = '1'
    game.events = [event]

    ib.update()

    event.type = pygame.KEYDOWN
    event.unicode = '.'
    game.events = [event]

    ib.update()

    event.type = pygame.KEYDOWN
    event.unicode = 'g'
    game.events = [event]

    ib.update()

    assert ib.text == '1.'
