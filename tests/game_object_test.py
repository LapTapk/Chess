from src.engine.renderer import Renderer
from src.engine.game_object import GameObject
from src.engine.input_box import InputBox


class GameObjectTest:
    def test_get_component_contains(self):
        comp1 = Renderer()
        comp2 = InputBox()
        go = GameObject()
        go.init(components=[comp1, comp2])
        found = go.get_component(Renderer)
        assert found == comp1

    def test_get_component_does_not_contain(self):
        go = GameObject()
        go.init(None)
        comp_go = go.get_component(Renderer)
        assert comp_go == None

    def test_add_component(self):
        go = GameObject()
        comp1 = Renderer()
        comp2 = InputBox()
        comp1.init(go, None)
        comp2.init(go, None, None)
        go.init(None)
        go.add_component(comp1)
        go.add_component(comp2)
        assert go.get_component(
            Renderer) != None and go.get_component(InputBox) != None
