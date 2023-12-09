from engine import game
from engine.scenes import create_start_scene
import sys

sys.path.extend(['.'])

game.init((1280, 720), 60)
game.cur_scene = create_start_scene()
game.run()
