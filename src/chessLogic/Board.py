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
        self.whiteKingPos = (3, 0)
        self.blackKingPos = (3, 7)


    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()
        print("###########################")

    def is_legal(self, frm, to):
        # проверка на края доски
        if to[0] < 0 or to[0] > 7 or to[1] < 0 or to[1] > 7:
            return False
        # проверка на съедение короля и фигур своего цвета
        if self.board[to[0]][to[1]].name in ('k', 'K') or \
            self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]].color:
            return False

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
        # проверка на возможность хода слоном
        if self.board[frm[0]][frm[1]].name in ('b', 'B'):
            if self.is_legal_b(frm, to):
                return True
            else:
                return False

        # проверка на возможность хода ферзём
        if self.board[frm[0]][frm[1]].name in ('q', 'Q'):
            if self.is_legal_q(frm, to):
                return True
            else:
                return False

        if self.board[frm[0]][frm[1]].name in ('k', 'K'):
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
        if (abs(frm[0] - to[0]) == 1 and abs(frm[1] - to[1]) == 2) or \
                (abs(frm[0] - to[0]) == 2 and abs(frm[1] - to[1]) == 1):
            return True
        else:
            return False

    def is_legal_b(self, frm, to):
        if abs(frm[0] - to[0]) != abs(frm[1] - to[1]):
            return False
        i_plus = 1 if frm[0] < to[0] else -1
        j_plus = 1 if frm[1] < to[0] else -1
        i = frm[0] + i_plus
        j = frm[1] + j_plus
        while i != to[0] and j != to[1]:
            if self.board[i][j].name != '.':
                return False
            i += i_plus
            j += j_plus
        return True

    def is_legal_r(self, frm, to):
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

    def is_legal_q(self, frm, to):
        # проверка равна проверке хода ладьи или слона
        if self.is_legal_r(frm, to) or self.is_legal_b(frm, to):
            return True
        else:
            return False

    def is_legal_k(self, frm, to):
        # проверка на шах
        # проверка на рокировку (добавить поле у короля на возможность рокировки)
        pass

    def is_checked_on_pos(self, pos, king_color):           #нужна проверка на вскрытый шах после отхода своей фигуры!!
        # проверка на короля противника, около клетки pos
        around = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for i, j in around:
            if (0 <= pos[0] + i <= 7) and (0 <= pos[1] + j <= 7) and \
                    self.board[pos[0] + i][pos[1] + j].name in ('k', 'K') and \
                    self.board[pos[0] + i][pos[1] + j].color != king_color:
                return True

        # проверка на шах по j
        for j in range(pos[1] - 1, -1, -1):
            if self.board[pos[0]][j].name == '.':
                continue
            if self.board[pos[0]][j].color == king_color:
                break
            else:
                if self.board[pos[0]][j].name in ('q', 'Q', 'r', 'R'):
                    return True
                if self.board[pos[0]][j].name in ('n', 'N', 'b', 'B', 'p', 'P', 'k', 'K'):
                    break

        for j in range(pos[1] + 1, 8):
            if self.board[pos[0]][j].name == '.':
                continue
            if self.board[pos[0]][j].color == king_color:
                break
            else:
                if self.board[pos[0]][j].name in ('q', 'Q', 'r', 'R'):
                    return True
                if self.board[pos[0]][j].name in ('n', 'N', 'b', 'B', 'p', 'P', 'k', 'K'):
                    break

        # проверка на шах по i
        for i in range(pos[0] - 1, -1, -1):
            if self.board[i][pos[1]].name == '.':
                continue
            if self.board[i][pos[1]].color == king_color:
                break
            else:
                if self.board[i][pos[1]].name in ('q', 'Q', 'r', 'R'):
                    return True
                if self.board[i][pos[1]].name in ('n', 'N', 'b', 'B', 'p', 'P', 'k', 'K'):
                    break
                '''
                if self.board[i][pos[1]].name in ('k', 'K') and i == pos[0] - 1:
                    return True
                else:
                    break
                    '''

        for i in range(pos[0] + 1, 8):
            if self.board[i][pos[1]].name == '.':
                continue
            if self.board[i][pos[1]].color == king_color:
                break
            else:
                if self.board[i][pos[1]].name in ('q', 'Q', 'r', 'R'):
                    return True
                if self.board[i][pos[1]].name in ('n', 'N', 'b', 'B', 'p', 'P', 'k', 'K'):
                    break

        # проверка на шах по диагоналям
        diag = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        for i_plus, j_plus in diag:
            i = pos[0] + i_plus
            j = pos[1] + j_plus

            # проверка на шах от пешек
            if (0 <= i <= 7) and (0 <= j <= 7) and \
                    j_plus == 1 and king_color == 'white' and self.board[i][j].name == 'p':
                return True
            if (0 <= i <= 7) and (0 <= j <= 7) and \
                    j_plus == -1 and king_color == 'black' and self.board[i][j].name == 'P':
                return True

            while (0 <= i <= 7) and (0 <= j <= 7):
                if self.board[i][j].name == '.':
                    i += i_plus
                    j += j_plus
                    continue
                if self.board[i][j].color == king_color:
                    break
                else:
                    if self.board[i][j].name in ('q', 'Q', 'b', 'B'):
                        return True
                    if self.board[i][j].name in ('n', 'N', 'r', 'R', 'p', 'P'):
                        break

        # проверка на шах от коней
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        knight_name = 'n' if king_color == 'white' else 'N'
        for i, j in directions:
            if (0 <= pos[0] + i <= 7) and (0 <= pos[1] + j <= 7) and \
                    self.board[pos[0] + i][pos[1] + j].name == knight_name:
                return True

        # прошли все проверки на шах - нет шаха
        return False


    def move(self, frm, to):
        self.board[frm[0]][frm[1]].position = to
        self.board[to[0]][to[1]] = self.board[frm[0]][frm[1]]
        self.board[frm[0]][frm[1]] = Figure.Figure()
        self.lastMovefrm = frm
        self.lastMoveto = to
        if self.colorMove == 'white':
            self.colorMove = 'black'
        else:
            self.colorMove = 'white'

    def try_move(self, frm, to):
        if not self.is_legal(frm, to):
            print("ILLLEGAL MOVE")
            return False


        self.move(frm, to)
        print("Move done!!!!!!!!!!!")
        return True
