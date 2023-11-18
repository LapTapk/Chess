import game
from scenes import create_test_scene

game.init((500, 500), 60)
game.set_cur_scene(create_test_scene())
game.run()
