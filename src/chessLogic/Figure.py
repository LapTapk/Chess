import json


class Figure():
    """класс фигуры"""

    name = '.'

    def __init__(self, color='white', position=(0, 0)):
        self.color = color
        self.position = position

    def showFigureConsole(self):
        """вывод фигуры на доску в консоль"""
        return self.name

    def registerFromColor(self):
        """меняет регистр имени взависимости от цвета фигуры"""
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
    """класс фигуры король"""

    name = 'k'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name


class Queen(Figure):
    """класс фигуры королева"""

    name = 'q'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name


class Rock(Figure):

    name = 'r'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name


class Bishop(Figure):

    name = 'b'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name


class Knight(Figure):

    name = 'n'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name


class Pawn(Figure):

    name = 'p'

    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = self.registerFromColor()

    def showFigureConsole(self):
        """вывод фигуры в консоль -
        белые в верхнем регистре, чёрные в нижнем"""
        return self.name
