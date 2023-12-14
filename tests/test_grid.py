from src.engine.grid import Grid, find_closest
from src.engine.vector2 import Vector2
from src.engine.game_object import GameObject


def convert_to_tuple(actual):
    return list(map(lambda x: list(map(lambda y: y.to_tuple(), x)), actual))

def test_get_points_1():
    go = GameObject()
    grid = Grid()

    go.init(None)
    grid.init(go, Vector2(200, 200), Vector2(2, 2))

    right = [[(0.0, 0.0), (0.0, 200.0)], [(200.0, 0.0), (200.0, 200.0)]]
    actual = convert_to_tuple(grid.get_points())
    assert actual == right

def test_get_points_2():
    grid = Grid()
    go = GameObject()
    go.init(None, Vector2(50, 25), components=[grid])
    grid.init(go, Vector2(300, 250), Vector2(3, 5))
    right = [[(50, 25), (50, 87.5), (50, 150), (50, 212.5), (50, 275)],
                [(200, 25), (200, 87.5), (200, 150), (200, 212.5), (200, 275)],
                [(350, 25), (350, 87.5), (350, 150), (350, 212.5), (350, 275)]]
    right = list(map(lambda x:
                        list(map(lambda y: tuple(float(i) for i in y), x)),
                    right))
    actual = convert_to_tuple(grid.get_points())
    assert actual == right

def test_find_closest():
    grid = Grid()
    go = GameObject()

    go.init(None, Vector2(50, 60), components=[grid])
    grid.init(go, Vector2(400, 300), Vector2(10, 8))

    closest = find_closest(grid, Vector2(280, 150))
    assert closest == Vector2(5, 2)