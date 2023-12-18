import json


class Figure():
    '''Класс шахматные фигуры'''

    '''имя фигуры'''
    name: str = '.'

    def __init__(self, color: str = 'neutral', position: tuple = (0, 0)):
        '''
        Создание фигуры
        :param color: цвет фигуры
        :param position: позиция, на которой создаётся фигура
        '''
        self.color: str = color
        self.position: tuple = position

    def showFigureConsole(self):
        '''
        Вывод имени фигуры на доску в консоль
        '''
        return self.name

    def registerFromColor(self):
        '''
        Меняет регистр имени в зависимости от цвета фигуры
        '''
        if self.color == 'white':
            return self.name.upper()
        else:
            return self.name.lower()

    def serialize(self):
        res = json.dumps(self, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
        res = f'{{"type": "{type(self).__name__}",\n' + res[1:]
        return res

    def deserialize(data):
        figure_types = {'Figure': Figure, 'Pawn': Pawn,
                        'Rock': Rock, 'Bishop': Bishop,
                        'Knight': Knight, 'Queen': Queen,
                        'King': King}
        cur_type = figure_types[data['type']]
        color = data['color']
        pos = data['position']
        return cur_type(color, pos)


class King(Figure):
    '''Класс фигуры король'''

    name = 'k'

    def __init__(self, color: str, position: tuple):
        '''
        Создание фигуры король
        :param color: цвет короля
        :param position: позиция короля
        '''
        super().__init__(color, position)
        self.name = self.registerFromColor()
        self.did_move = False


class Queen(Figure):
    '''Класс фигуры королева'''

    name = 'q'

    def __init__(self, color, position):
        '''
        Создание фигуры ферзь
        :param color: цвет ферзя
        :param position: позиция ферзя
        '''
        super().__init__(color, position)
        self.name = self.registerFromColor()


class Rock(Figure):
    name = 'r'

    def __init__(self, color, position):
        '''
        Создание фигуры ладья
        :param color: цвет ладьи
        :param position: позиция ладьи
        '''
        super().__init__(color, position)
        self.name = self.registerFromColor()
        self.did_move = False


class Bishop(Figure):
    name = 'b'

    def __init__(self, color, position):
        '''
        Создание фигуры слон
        :param color: цвет слона
        :param position: позиция слона
        '''
        super().__init__(color, position)
        self.name = self.registerFromColor()


class Knight(Figure):
    name = 'n'

    def __init__(self, color, position):
        '''
        Создание фигуры конь
        :param color: цвет коня
        :param position: позиция коня
        '''
        super().__init__(color, position)
        self.name = self.registerFromColor()


class Pawn(Figure):
    name = 'p'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def transformation(self, board, figure='q'):
        '''
        Превращение пешки в другие фигуры, при достижении противоположного кра доски
        :param board: доска, на которой стоит пешка
        :param figure: фигура, в которую должна превратиться пешка
        '''
        if figure in ('q', 'Q'):
            board[self.position[0]][self.position[1]] = Queen(self.color, self.position)
        if figure in ('k', 'K'):
            board[self.position[0]][self.position[1]] = King(self.color, self.position)
        if figure in ('b', 'B'):
            board[self.position[0]][self.position[1]] = Bishop(self.color, self.position)
        if figure in ('n', 'N'):
            board[self.position[0]][self.position[1]] = Knight(self.color, self.position)
        if figure in ('r', 'R'):
            board[self.position[0]][self.position[1]] = Rock(self.color, self.position)
