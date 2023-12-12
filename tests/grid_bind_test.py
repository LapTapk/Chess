from src.engine.grid import GridBinder, Grid
from src.engine.game_object import GameObject
from src.engine.vector2 import Vector2


class GridBindTest:
    grid = Grid()
    go = GameObject()
    grid.init(Vector2(400, 300), Vector2(10, 7))

    def test_bind_1(self):
        binder = GridBinder()
        go = GameObject()
        binder.init(GridBindTest.grid, Vector2(3, 5))
        go.init(components=[binder])

        binder.update()

        right = (143.33333333333331, 270.0)
        actual = go.position.to_tuple()
        assert actual == right

    def test_bind_2(self):
        binder = GridBinder()
        go = GameObject()
        binder.init(GridBindTest.grid, Vector2(5, 6))
        go.init(components=[binder])

        binder.update()

        right = (1353, 135)
        actual = go.position.to_tuple()
        assert actual == right
