from src.engine.game_object import Scene, GameObject
import pygame
from src.engine.renderer import Renderer
from src.engine.vector2 import Vector2
import utils
 
utils.game_pseudoinit()

def test_update():
    scene = Scene()
    go1 = GameObject()
    go2 = GameObject()
    rend1 = Renderer()
    rend2 = Renderer()

    updates = []
    rend1.update = lambda: updates.append('go1')
    rend2.update = lambda: updates.append(rend2)
    go1.init(scene, components=[rend1], children=[go2])
    go2.init(scene, components=[rend2])

    scene.init(go1)
    scene.update()
    assert updates == ['go1', rend2]

def test_add_object():
    scene = Scene()
    go1 = GameObject()
    go2 = GameObject()

    scene.init()
    go1.init(scene)
    go2.init(scene)

    scene.add_object(go1)
    scene.add_object(go2)
    assert scene.objects == [go1, go2]

def test_at_point_overlay():
    scene = Scene()
    go1 = GameObject()
    go2 = GameObject()
    rend1 = Renderer()
    rend2 = Renderer()

    rend1.init(go1, pygame.surface.Surface((10, 7)))
    rend2.init(go2, pygame.surface.Surface((5, 2)))

    pos1 = Vector2(40, 70)
    go1.init(scene, pos=pos1, components=[rend1])

    pos2 = Vector2(44, 72)
    go2.init(scene, pos=pos2, components=[rend2])

    scene.init(go1, go2)
    print(rend1.get_rect(), rend2.get_rect())
    ap = scene.at_point((44, 72))
    assert ap == [go1, go2]

def test_at_point_children():
    scene = Scene()
    go1 = GameObject()
    go2 = GameObject()
    rend1 = Renderer()
    rend2 = Renderer()

    rend1.init(go1, pygame.surface.Surface((2, 2)))
    rend2.init(go2, pygame.surface.Surface((6, 7)))

    pos1 = Vector2(10, 45)
    go1.init(scene, pos=pos1, components=[rend1], children=[go2])

    pos2 = Vector2(21, 84)
    go2.init(scene, pos=pos2, components=[rend2])

    scene.init(go1)
    ap = scene.at_point((22, 85))
    assert ap == [go2]