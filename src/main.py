from engine import game
from engine.scenes import create_start_scene
import sys

sys.path.extend(['.'])

game.init((500, 500), 20, 'game_data.json')
game.cur_scene = create_start_scene()
game.run()
