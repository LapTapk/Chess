import game
from scenes import create_start_scene

game.init((1280, 720), 60)
game.cur_scene = create_start_scene()
game.run()
