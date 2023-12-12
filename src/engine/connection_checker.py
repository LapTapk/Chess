from . import game, scenes

class ConnectionChecker:
    def update(self):
        if game.clnt != None and game.clnt.get_conn() == 2:
            game.cur_scene = scenes.create_chess_scene()