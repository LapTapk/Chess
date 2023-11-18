from game import Game
from scenes import create_test_scene

game = Game((500, 500), 60)
game.cur_scene = create_test_scene()
game.run()