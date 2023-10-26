import unittest
import engine.renderer as renderer
from engine.game_object import GameObject


class GameObjectTest(unittest.TestCase):
    def test_get_component_contains(self):
        comp = renderer.Renderer(None, None)
        go = GameObject(components=[comp])
        comp_go = go.get_component(renderer.Renderer)
        self.assertEqual(comp_go, comp)

    def test_get_component_does_not_contain(self):
        go = GameObject()
        comp_go = go.get_component(renderer.Renderer)
        self.assertIsNone(comp_go)
