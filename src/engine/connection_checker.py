from . import game, scenes


class ConnectionChecker:
    '''Компонент, проверяющий, подключилось ли достаточное число игроков,
    и переключающий в таком случае сцену на игровую'''

    def update(self) -> None:
        '''Метод кадра компоента'''
        if game.clnt != None and game.clnt.get_conn() == 2:
            game.cur_scene = scenes.create_chess_scene()
