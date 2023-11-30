import game
from scenes import *

game.init((1280, 720), 60)
game.cur_scene = create_start_menu_scene()
game.run()
