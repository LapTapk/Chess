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
        self.lastMovefrm = (0, 0)
        self.lastMoveto = (0, 0)
        self.board = [[Figure.Figure() for j in range(self.lenght)]
                      for i in range(self.lenght)]
        self.board = self.startPosition()
        self.colorMove = 'white'


    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()
        print("###########################")

    def is_legal(self, frm, to):
        # проверка на правильный цвет выбраннй фигуры
        if self.colorMove != self.board[frm[0]][frm[1]].color:
            return False

        # проверка на возможность хода пешкой
        if self.board[frm[0]][frm[1]].name in ('p', 'P'):
            if self.is_legal_p(frm, to):
                if to[1] in (0, 7):
                    self.board[frm[0]][frm[1]].transformation(self.board)
                return True
            else:
                return False

        # проверка на возмжность хода конём
        if self.board[frm[0]][frm[1]].name in ('n', 'N'):
            if self.is_legal_n(frm, to):
                return True
            else:
                return False

        # проверка на возможность хода ладьёй
        if self.board[frm[0]][frm[1]].name in ('r', 'R'):
            if self.is_legal_r(frm, to):
                return True
            else:
                return False



        pass

        # return self.board[to.x][to.y].name == '.'

    def is_legal_p(self, frm, to):
        if abs(frm[1] - to[1]) > 2 or abs(frm[1] - to[1]) < 1 or \
                (abs(frm[1] - to[1]) == 2 and (frm[1] not in (1, 6))) or \
                abs(frm[0] - to[0]) > 1:
            return False
        # проверка на правильность направления хода
        if self.colorMove == 'white' and frm[1] >= to[1]:
            return False
        if self.colorMove == 'black' and frm[1] <= to[1]:
            return False

        # пешка идёт вперёд
        if frm[0] == to[0]:
            if abs(frm[1] - to[1]) == 1 and self.board[to[0]][to[1]].name == '.':
                return True
            if self.colorMove == 'white':
                if abs(frm[1] - to[1]) == 2 and self.board[to[0]][to[1]].name == '.' and \
                        self.board[to[0]][to[1] - 1].name == '.':
                    return True
            elif abs(frm[1] - to[1]) == 2 and self.board[to[0]][to[1]].name == '.' and \
                    self.board[to[0]][to[1] + 1].name == '.':
                return True
            else:
                return False
        # пешка бьёт другую фигуру
        else:
            # есть фигуры своего цвета нельзя
            if self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]]:
                return False
            # проверка на взятие на проходе (убирает взятую на проходе пешку в проверке на ход)
            if self.board[to[0]][to[1]].name == '.':
                if self.board[to[0]][frm[1]].name in ('p' or 'P') and \
                        self.board[to[0]][frm[1]].color != self.board[frm[0]][frm[1]].color and \
                        self.lastMoveto == (to[0], frm[1]) and \
                        abs(self.lastMovefrm[1] - self.lastMoveto[1]) == 2:
                    self.board[to[0]][frm[1]] = Figure.Figure()
                    #self.lastMoveto == to and self.lastMovefrm == frm
                    return True
                else:
                    return False
            if self.board[to[0]][to[1]].name in ('k', 'K'):
                return False
            return True

    def is_legal_n(self, frm, to):
        if to[0] < 0 or to[0] > 7 or to[1] < 0 or to[1] > 7:
            return False
        if self.board[to[0]][to[1]].name in ('k', 'K') or \
            self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]].color:
            return False
        if (abs(frm[0] - to[0]) == 1 and abs(frm[1] - to[1]) == 2) or \
                (abs(frm[0] - to[0]) == 2 and abs(frm[1] - to[1]) == 1):
            return True
        else:
            return False

    def is_legal_r(self, frm, to):
        if to[0] < 0 or to[0] > 7 or to[1] < 0 or to[1] > 7:
            return False
        if self.board[to[0]][to[1]].name in ('k', 'K') or \
                self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]].color:
            return False
        if frm[0] != to[0] and frm[1] != to[1]:
            return False
        if frm[0] == to[0]:
            for i in range(min(frm[1], to[1]) + 1, max(frm[1], to[1])):
                if self.board[frm[0]][i].name != '.':
                    return False
            return True
        if frm[1] == to[1]:
            for i in range(min(frm[0], to[0]) + 1, max(frm[0], to[0])):
                if self.board[i][frm[1]].name != '.':
                    return False
            return True


    def move(self, frm, to):
        self.board[frm[0]][frm[1]].position = to
        self.board[to[0]][to[1]] = self.board[frm[0]][frm[1]]
        self.board[frm[0]][frm[1]] = Figure.Figure()

    def try_move(self, frm, to):
        if not self.is_legal(frm, to):
            print("ILLLEGAL MOVE")
            return False

        self.lastMovefrm = frm
        self.lastMoveto = to
        self.move(frm, to)
        if self.colorMove == 'white':
            self.colorMove = 'black'
        else:
            self.colorMove = 'white'

        print("Move done!!!!!!!!!!!")
        return True
