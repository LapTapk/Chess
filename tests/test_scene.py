from src.engine.game_object import Scene, GameObject
from src.engine.renderer import Renderer
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
