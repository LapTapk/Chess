import Figure


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
                    self.board[i][j] = Figure.Pawn("white", (i, j))
                    continue
                if i == 6:
                    self.board[i][j] = Figure.Pawn("black", (i, j))
                    continue

                if i == 0:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[i][j] = Figure.Rock("white", (i, j))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[i][j] = Figure.Knight("white", (i, j))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[i][j] = Figure.Bishop("white", (i, j))
                    """создание королевы"""
                    if j == 4:
                        self.board[i][j] = Figure.Queen("white", (i, j))
                    """создание короля"""
                    if j == 3:
                        self.board[i][j] = Figure.King("white", (i, j))

                if i == 7:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[i][j] = Figure.Rock("black", (i, j))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[i][j] = Figure.Knight("black", (i, j))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[i][j] = Figure.Bishop("black", (i, j))
                    """создание королевы"""
                    if j == 4:
                        self.board[i][j] = Figure.Queen("black", (i, j))
                    """создание короля"""
                    if j == 3:
                        self.board[i][j] = Figure.King("black", (i, j))
        return self.board

    def __init__(self):
        self.board = [[Figure.Figure() for j in range(self.lenght)] for i in range(self.lenght)]
        self.board = self.startPosition()

    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()


b = Board()
b.showBoardConsole()
