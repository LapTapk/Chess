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

    def transformation(self, board, figure='q'):
        # пока всегда превращяется в ферзя
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

