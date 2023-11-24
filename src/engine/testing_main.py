import game
from scenes import *

game.init((1000, 700), 60)
game.set_cur_scene(create_chess_scene())
game.run()
