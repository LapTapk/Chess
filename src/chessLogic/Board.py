from . import Figure


class Board(object):
    lenght = 8

    def startPosition(self):
        """
        i - строки
        j - столбцы
        0, 1 - белые фигуры
        6, 7 - чёрные фигуры
        """
        for i in range(self.lenght):
            for j in range(self.lenght):
                """создание пешек"""
                if i == 1:
                    self.board[j][i] = Figure.Pawn("white", (i, j))
                    continue
                if i == 6:
                    self.board[j][i] = Figure.Pawn("black", (i, j))
                    continue

                if i == 0:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[j][i] = Figure.Rock("white", (i, j))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[j][i] = Figure.Knight("white", (i, j))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[j][i] = Figure.Bishop("white", (i, j))
                    """создание королевы"""
                    if j == 4:
                        self.board[j][i] = Figure.Queen("white", (i, j))
                    """создание короля"""
                    if j == 3:
                        self.board[j][i] = Figure.King("white", (i, j))

                if i == 7:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[j][i] = Figure.Rock("black", (i, j))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[j][i] = Figure.Knight("black", (i, j))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[j][i] = Figure.Bishop("black", (i, j))
                    """создание королевы"""
                    if j == 4:
                        self.board[j][i] = Figure.Queen("black", (i, j))
                    """создание короля"""
                    if j == 3:
                        self.board[j][i] = Figure.King("black", (i, j))
        return self.board

    def __init__(self):
        self.board = [[Figure.Figure() for j in range(self.lenght)] for i in range(self.lenght)]
        self.board = self.startPosition()

    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()

    def is_legal(self, frm, to):
        return self.board[to.x][to.y].name == '.'
