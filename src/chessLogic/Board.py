from . import Figure
import copy


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
                    if j == 3:
                        self.board[j][i] = Figure.Queen("white", (j, i))
                    """создание короля"""
                    if j == 4:
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
                    if j == 3:
                        self.board[j][i] = Figure.Queen("black", (j, i))
                    """создание короля"""
                    if j == 4:
                        self.board[j][i] = Figure.King("black", (j, i))
        return self.board

    def __init__(self):
        self.lastMovefrm = (0, 0)
        self.lastMoveto = (0, 0)
        self.board = [[Figure.Figure() for j in range(self.lenght)]
                      for i in range(self.lenght)]
        self.board = self.startPosition()
        self.colorMove = 'white'
        self.whiteKingPos = (4, 0)
        self.blackKingPos = (4, 7)

    def showBoardConsole(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()
        print("###########################")

    def is_legal(self, frm, to):
        # проверка на отсутсвие хода
        if frm[0] == to[0] and frm[1] == to[1]:
            self.returning_figure(frm)
            return False
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
            color = self.colorMove
            if self.is_legal_p(frm, to) and self.is_opened_check(frm, to, color):
                if to[1] in (0, 7):
                    self.board[frm[0]][frm[1]].transformation(self.board)
                return True
            else:
                return False

        # проверка на возмжность хода конём
        if self.board[frm[0]][frm[1]].name in ('n', 'N'):
            color = self.colorMove
            if self.is_legal_n(frm, to) and self.is_opened_check(frm, to, color):
                return True
            else:
                return False

        # проверка на возможность хода ладьёй
        if self.board[frm[0]][frm[1]].name in ('r', 'R'):
            color = self.colorMove
            if self.is_legal_r(frm, to) and self.is_opened_check(frm, to, color):
                return True
            else:
                return False
        # проверка на возможность хода слоном
        if self.board[frm[0]][frm[1]].name in ('b', 'B'):
            color = self.colorMove
            if self.is_legal_b(frm, to) and self.is_opened_check(frm, to, color):
                return True
            else:
                return False

        # проверка на возможность хода ферзём
        if self.board[frm[0]][frm[1]].name in ('q', 'Q'):
            color = self.colorMove
            if self.is_legal_q(frm, to) and self.is_opened_check(frm, to, color):
                return True
            else:
                return False

        if self.board[frm[0]][frm[1]].name in ('k', 'K'):
            if self.is_legal_k(frm, to):
                return True
            else:
                return False

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
                    # self.lastMoveto == to and self.lastMovefrm == frm
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
        # проверка на шах при ходе на 1 клетку
        if abs(frm[0] - to[0]) < 2 and abs(frm[1] - to[1]) < 2 and \
                not self.is_checked_on_pos(to, self.board[frm[0]][frm[1]].color):
            return True
        # проверка на рокировку (добавить поле у короля на возможность рокировки)
        if abs(frm[0] - to[0]) == 2 and self.is_castling_legal(frm, to):
            self.colorMove = 'white'
            return True
        else:
            return False

    def is_checked_on_pos(self, pos, king_color):
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

        # прошли все проверки на шах -> нет шаха
        return False

    def is_opened_check(self, frm, to, color):
        board = copy.deepcopy(self)
        board.move(frm, to)
        kingPos = self.whiteKingPos if color == 'white' else self.blackKingPos
        if board.is_checked_on_pos(kingPos, color):
            return False
        else:
            return True

    def is_castling_legal(self, frm, to):
        kingColor = self.colorMove
        if self.is_checked_on_pos(frm, kingColor):
            return False
        if self.board[frm[0]][frm[1]].did_move:
            return False
        if self.board[frm[0]][frm[1]].color == 'white':
            if frm[0] != 4 and frm[1] != 0:
                return False
            # (7, 0), (0, 0) - координаты ладей
            if to[0] == 6 and to[1] == 0 and self.board[7][0].name == 'R' and \
                    not self.board[7][0].did_move and self.board[5][0].name == '.' and \
                    self.board[6][0].name == '.' and not self.is_checked_on_pos((5, 0), 'white') and \
                    not self.is_checked_on_pos((6, 0), 'white'):
                # рокировка будет сделана, поэтому переместим ладью сразу из проверки
                self.move((7, 0), (5, 0))
                return True
            if to[0] == 2 and to[1] == 0 and self.board[0][0].name == 'R' and \
                    not self.board[0][0].did_move and self.board[3][0].name == '.' and \
                    self.board[2][0].name == '.' and self.board[1][0].name == '.' and \
                    not self.is_checked_on_pos((3, 0), 'white') and \
                    not self.is_checked_on_pos((2, 0), 'white') and \
                    not self.is_checked_on_pos((1, 0), 'white'):
                # рокировка будет сделана, поэтому переместим ладью сразу из проверки
                self.move((0, 0), (3, 0))
                return True
            return False
        else:
            if frm[0] != 4 and frm[1] != 7:
                return False
            # (7, 7), (0, 7) - координаты ладей
            if to[0] == 6 and to[1] == 7 and self.board[7][7].name == 'r' and \
                    not self.board[7][7].did_move and self.board[5][7].name == '.' and \
                    self.board[6][7].name == '.' and not self.is_checked_on_pos((5, 7), 'black') and \
                    not self.is_checked_on_pos((6, 7), 'black'):
                # рокировка будет сделана, поэтому переместим ладью сразу из проверки
                self.move((7, 7), (5, 7))
                return True
            if to[0] == 2 and to[0] == 7 and self.board[0][7].name == 'r' and \
                    not self.board[0][7].did_move and self.board[3][7].name == '.' and \
                    self.board[2][7].name == '.' and self.board[1][7].name == '.' and \
                    not self.is_checked_on_pos((3, 7), 'black') and \
                    not self.is_checked_on_pos((2, 7), 'black') and \
                    not self.is_checked_on_pos((1, 7), 'black'):
                # рокировка будет сделана, поэтому переместим ладью сразу из проверки
                self.move((0, 7), (3, 7))
                return True
            return False

    def is_game_over(self, color):
        kingPos = self.whiteKingPos if color == 'white' else self.blackKingPos
        for i in range(8):
            for j in range(8):
                if not self.board[i][j].color == color:
                    continue
                else:
                    #  проверка пешек на возможность ходить
                    if self.board[i][j].name in ('p', 'P'):
                        if color == 'white':
                            if self.is_legal((i, j), (i, j + 1)) or \
                                    self.is_legal((i, j), (i, j + 2)) or \
                                    self.is_legal((i, j), (i + 1, j + 1)) or \
                                    self.is_legal((i, j), (i - 1, j + 1)):
                                return False
                        elif self.is_legal((i, j), (i, j - 1)) or \
                                self.is_legal((i, j), (i, j - 2)) or \
                                self.is_legal((i, j), (i + 1, j - 1)) or \
                                self.is_legal((i, j), (i - 1, j - 1)):
                            return False
                    # проверка коней на возможность ходить
                    if self.board[i][j].name in ('n', 'N'):
                        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
                        for i_plus, j_plus in directions:
                            if 0 <= i + i_plus <= 7 and 0 <= j + j_plus <= 7 and \
                                    self.is_legal((i, j), (i + i_plus, j + j_plus)):
                                return False
                    # проверка ладей и ферзя на возможность ходить
                    if self.board[i][j].name in ('r', 'R', 'q', 'Q'):
                        for j_ in range(j + 1, 8):
                            if self.is_legal((i, j), (i, j_)):
                                return False
                        for j_ in range(j - 1, -1, -1):
                            if self.is_legal((i, j), (i, j_)):
                                return False
                        for i_ in range(i + 1, 8):
                            if self.is_legal((i, j), (i_, j)):
                                return False
                        for i_ in range(i - 1, -1, -1):
                            if self.is_legal((i, j), (i_, j)):
                                return False
                    # проверка слонов и ферзя на возможность ходить
                    if self.board[i][j].name in ('b', 'B', 'q', 'Q'):
                        diag = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                        for i_plus, j_plus in diag:
                            i_ = i + i_plus
                            j_ = j + j_plus
                            while 0 <= i_ <= 7 and 0 <= j_ <= 7:
                                if self.is_legal((i, j), (i_, j_)):
                                    return False
                                i_ += i_plus
                                j += j_plus
                    # проверка короля на возможность ходить
                    if self.board[i][j].name in ('k', 'K'):
                        around = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
                        for i_plus, j_plus in around:
                            if 0 <= i + i_plus <= 7 and 0 <= j + j_plus <= 7 and \
                                    self.is_legal((i, j), (i + i_plus, j + j_plus)):
                                return False
        if not self.is_checked_on_pos(kingPos, color):
            return 'stalemate'
        else:
            return 'checkmate'

    def returning_figure(self, frm):
        self.board[frm[0]][frm[1]] = self.board[frm[0]][frm[1]]

    def move(self, frm, to):
        self.board[frm[0]][frm[1]].position = to
        if self.board[frm[0]][frm[1]].name in ('k', 'K', 'r', 'R') and not self.board[frm[0]][frm[1]].did_move:
            self.board[frm[0]][frm[1]].did_move = True
        if self.board[frm[0]][frm[1]].name == 'K':
            self.whiteKingPos = to
        if self.board[frm[0]][frm[1]].name == 'k':
            self.blackKingPos = to
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
