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
                    self.board[j][i] = Figure.Pawn("white", (j, i))
                    continue
                if i == 6:
                    self.board[j][i] = Figure.Pawn("black", (j, i))
                    continue

                if i == 0:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[j][i] = Figure.Rock("white", (j, i))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[j][i] = Figure.Knight("white", (j, i))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[j][i] = Figure.Bishop("white", (j, i))
                    """создание королевы"""
                    if j == 4:
                        self.board[j][i] = Figure.Queen("white", (j, i))
                    """создание короля"""
                    if j == 3:
                        self.board[j][i] = Figure.King("white", (j, i))

                if i == 7:
                    """создание ладей"""
                    if j == 0 or j == 7:
                        self.board[j][i] = Figure.Rock("black", (j, i))
                    """создание коней"""
                    if j == 1 or j == 6:
                        self.board[j][i] = Figure.Knight("black", (j, i))
                    """создание слонов"""
                    if j == 2 or j == 5:
                        self.board[j][i] = Figure.Bishop("black", (j, i))
                    """создание королевы"""
                    if j == 4:
                        self.board[j][i] = Figure.Queen("black", (j, i))
                    """создание короля"""
                    if j == 3:
                        self.board[j][i] = Figure.King("black", (j, i))
        return self.board

    def __init__(self):
        self.board = [[Figure.Figure() for j in range(self.lenght)]
                      for i in range(self.lenght)]
        self.board = self.startPosition()

    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()

    def is_legal(self, frm, to):
        return self.board[to.x][to.y].name == '.'

    def move(self, frm, to):
        pass

    def try_move(self, frm, to):
        if not self.is_legal(frm, to):
            return False

        self.move(frm, to)
        return True
    

    def serialize(self):
        res = '{"board": ['
        for i in range(Board.lenght):
            res += '['
            for j in range(Board.lenght):
                ser = self.board[i][j].serialize()
                res += ser + (',' if j != 7 else '')
                
            res += ']' + (',' if i != 7 else '')
        res += ']}'
        print(res)
        return res
    
    def deserialize(data):
        board = data['board']
        res = Board()

        for i in range(Board.lenght):
            for j in range(Board.lenght):
                figure = Figure.Figure.deserialize(board[i][j])
                res.board[i][j] = figure
        
        return res