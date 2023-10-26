import unittest
from engine.grid import GridBind, Grid
from engine.game_object import GameObject
from engine.vector2 import Vector2


class GridBindTest(unittest.TestCase):
    grid = Grid(Vector2(400, 300), Vector2(10, 7))
    go = GameObject(Vector2(10, 20), components=[grid])

    def test_bind_1(self):
        binder = GridBind(GridBindTest.grid, Vector2(3, 5))
        go = GameObject(components=[binder])

        binder.update()

        right = (143.33333333333331, 270.0)
        actual = go.position.to_tuple()
        self.assertEqual(actual, right)

    def test_bind_2(self):
        binder = GridBind(GridBindTest.grid, Vector2(5, 6))
        go = GameObject(components=[binder])

        binder.update()

        right = (1353, 135)
        actual = go.position.to_tuple()
        self.assertNotEqual(actual, right)
