from src.engine.grid import GridBinder, Grid
from src.engine.game_object import GameObject
from src.engine.vector2 import Vector2
import utils


utils.game_pseudoinit()


def test_bind():
    grid = Grid()
    go1 = GameObject()
    go1.init(None)
    grid.init(go1, Vector2(400, 300), Vector2(10, 7))

    binder = GridBinder()
    go = GameObject()
    binder.init(go, grid, Vector2(3, 5))
    go.init(None, components=[binder])

    binder.update()

    right = (133.33333333333331, 250.0)
    actual = go.position.to_tuple()
    assert actual == right
