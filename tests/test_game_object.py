from src.engine.game_object import GameObject
from src.engine.renderer import Renderer
from src.engine.input_box import InputBox
import utils


utils.game_pseudoinit()


def test_get_component_valid():
    go = GameObject()
    rend = Renderer()
    ib = InputBox()

    ib.init(go, None, None)
    rend.init(go, None)
    go.init(None, components=[ib, rend])
    assert go.get_component(Renderer) == rend


def test_get_component_nonvalid():
    go = GameObject()
    ib = InputBox()

    ib.init(go, None, None)
    go.init(None, components=[ib])
    assert go.get_component(Renderer) == None


def test_add_component():
    go = GameObject()
    ib = InputBox()

    go.init(None)
    ib.init(go, None, None)

    go.add_component(ib)
    assert go.get_component(InputBox) == ib
