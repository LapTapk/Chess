import unittest
from engine.grid import Grid
from engine.vector2 import Vector2
from engine.game_object import GameObject


class GridByCapacityTest(unittest.TestCase):
    def convert_to_tuple(actual):
        return list(map(lambda x: list(map(lambda y: y.to_tuple(), x)), actual))

    def test_get_points_1(self):
        grid = Grid(Vector2(200, 200), Vector2(2, 2))
        go = GameObject(Vector2(0, 0), components=[grid])
        right = [[(0.0, 0.0), (0.0, 200.0)], [(200.0, 0.0), (200.0, 200.0)]]
        actual = GridByCapacityTest.convert_to_tuple(grid.get_points())
        self.assertEqual(actual, right)

    def test_get_points_2(self):
        grid = Grid(Vector2(300, 250), Vector2(3, 5))
        go = GameObject(Vector2(50, 25), components=[grid])
        right = [[(50, 25), (50, 87.5), (50, 150), (50, 212.5), (50, 275)],
                 [(200, 25), (200, 87.5), (200, 150), (200, 212.5), (200, 275)],
                 [(350, 25), (350, 87.5), (350, 150), (350, 212.5), (350, 275)]]
        right = list(map(lambda x:
                         list(map(lambda y: tuple(float(i) for i in y), x)),
                     right))
        actual = GridByCapacityTest.convert_to_tuple(grid.get_points())
        self.assertEqual(actual, right)


if __name__ == "__main__":
    unittest.main()
