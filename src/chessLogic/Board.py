from . import Figure
from typing import *
import copy


class Board(object):
    '''
    Объект шахманой доски
    '''

    def startPosition(self):
        '''
        Расппологает фигуры по начальным позициям
        Возвращает доску с начальной расстановкой шахматных фигур
        '''

        # i - столбцы
        # j - стороки
        # 0, 1 - белые фигуры
        # 6, 7 - чёрные фигуры
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
        '''
        Создаёт объект шахматной доски
        '''

        self.lenght: int = 8
        '''длина стороны доски в клетках'''
        self.lastMovefrm: tuple = (0, 0)
        '''координаты начального положения фигуры, которая сделала последний ход'''
        self.lastMoveto: tuple = (0, 0)
        '''координаты конечного положения фигуры, которая сделала последний ход'''
        self.board: [[Figure]] = [[Figure.Figure() for j in range(self.lenght)]
                                  for i in range(self.lenght)]
        '''доска, каждая ячейка двумерного массива эквивалентна клетке доски'''
        # self.board = self.startPosition()
        self.colorMove: str = 'white'
        '''состояние, показывающее какой из игроков ходит (по цвету)'''
        self.whiteKingPos: tuple = (4, 0)
        '''положение белого короля'''
        self.blackKingPos: tuple = (4, 7)
        '''положение чрного короля'''

    def showBoardConsole(self):
        '''
        Выводит доску в консоль (для тестирования)
        '''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j].showFigureConsole(), end='')
            print()
        print("###########################")

    def is_legal(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода фигуры с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти фигура
        :param to: клетка, на которую пытается попасть фигура
        :return: True - если ход возможен, False - если ход невозможен
        '''
        '''проверка на отсутсвие хода'''
        if frm[0] == to[0] and frm[1] == to[1]:
            self.returning_figure(frm)
            return False
        '''проверка на края доски'''
        if to[0] < 0 or to[0] > 7 or to[1] < 0 or to[1] > 7:
            return False
        '''проверка на съедение короля и фигур своего цвета'''
        if self.board[to[0]][to[1]].name in ('k', 'K') or \
                self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]].color:
            return False

        '''проверка на правильный цвет выбраннй фигуры'''
        if self.colorMove != self.board[frm[0]][frm[1]].color:
            return False

        '''проверка на возможность хода пешкой'''
        if self.board[frm[0]][frm[1]].name in ('p', 'P'):
            color = self.colorMove
            if self.is_legal_p(frm, to) and not self.is_opened_check(frm, to, color):
                if to[1] in (0, 7):
                    self.board[frm[0]][frm[1]].transformation(self.board)
                return True
            else:
                return False

        '''проверка на возмжность хода конём'''
        if self.board[frm[0]][frm[1]].name in ('n', 'N'):
            color = self.colorMove
            if self.is_legal_n(frm, to) and not self.is_opened_check(frm, to, color):
                return True
            else:
                return False

        '''проверка на возможность хода ладьёй'''
        if self.board[frm[0]][frm[1]].name in ('r', 'R'):
            color = self.colorMove
            if self.is_legal_r(frm, to) and not self.is_opened_check(frm, to, color):
                return True
            else:
                return False
        '''проверка на возможность хода слоном'''
        if self.board[frm[0]][frm[1]].name in ('b', 'B'):
            color = self.colorMove
            if self.is_legal_b(frm, to) and not self.is_opened_check(frm, to, color):
                return True
            else:
                return False

        '''проверка на возможность хода ферзём'''
        if self.board[frm[0]][frm[1]].name in ('q', 'Q'):
            color = self.colorMove
            if self.is_legal_q(frm, to) and not self.is_opened_check(frm, to, color):
                return True
            else:
                return False
        '''проверка на возможнось хода королём'''
        if self.board[frm[0]][frm[1]].name in ('k', 'K'):
            if self.is_legal_k(frm, to):
                return True
            else:
                return False

    def is_legal_p(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода пешки с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти пешка
        :param to: клетка, на которую пытается попасть пешка
        :return: True - если ход возможен, False - если ход невозможен
        '''
        if abs(frm[1] - to[1]) > 2 or abs(frm[1] - to[1]) < 1 or \
                (abs(frm[1] - to[1]) == 2 and (frm[1] not in (1, 6))) or \
                abs(frm[0] - to[0]) > 1:
            return False
        '''проверка на правильность направления хода'''
        if self.colorMove == 'white' and frm[1] >= to[1]:
            return False
        if self.colorMove == 'black' and frm[1] <= to[1]:
            return False

        '''пешка идёт вперёд'''
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
        else:
            '''пешка бьёт другую фигуру'''

            '''есть фигуры своего цвета нельзя'''
            if self.board[to[0]][to[1]].color == self.board[frm[0]][frm[1]]:
                return False
            '''проверка на взятие на проходе (убирает взятую на проходе пешку в проверке на ход)'''
            if self.board[to[0]][to[1]].name == '.':
                if self.board[to[0]][frm[1]].name in ('p' or 'P') and \
                        self.board[to[0]][frm[1]].color != self.board[frm[0]][frm[1]].color and \
                        self.lastMoveto == (to[0], frm[1]) and \
                        abs(self.lastMovefrm[1] - self.lastMoveto[1]) == 2:
                    self.board[to[0]][frm[1]] = Figure.Figure()
                    return True
                else:
                    return False
            if self.board[to[0]][to[1]].name in ('k', 'K'):
                return False
            return True

    def is_legal_n(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода коня с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти коня
        :param to: клетка, на которую пытается попасть коня
        :return: True - если ход возможен, False - если ход невозможен
        '''
        if (abs(frm[0] - to[0]) == 1 and abs(frm[1] - to[1]) == 2) or \
                (abs(frm[0] - to[0]) == 2 and abs(frm[1] - to[1]) == 1):
            return True
        else:
            return False

    def is_legal_b(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода слона с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти слона
        :param to: клетка, на которую пытается попасть слона
        :return: True - если ход возможен, False - если ход невозможен
        '''
        if abs(frm[0] - to[0]) != abs(frm[1] - to[1]):
            return False
        i_plus = 1 if frm[0] < to[0] else -1
        j_plus = 1 if frm[1] < to[1] else -1
        i = frm[0] + i_plus
        j = frm[1] + j_plus
        while i != to[0] and j != to[1]:
            if self.board[i][j].name != '.':
                return False
            i += i_plus
            j += j_plus
        return True

    def is_legal_r(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода ладья с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти ладья
        :param to: клетка, на которую пытается попасть ладья
        :return: True - если ход возможен, False - если ход невозможен
        '''
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

    def is_legal_q(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода ферзя с позиции frm на позицию to
        (состоит из проверки возможности хода ладьи и слона)

        :param frm: клетка, с которой пытается пойти ферзя
        :param to: клетка, на которую пытается попасть ферзя
        :return: True - если ход возможен, False - если ход невозможен
        '''

        '''проверка равна проверке хода ладьи или слона'''
        if self.is_legal_r(frm, to) or self.is_legal_b(frm, to):
            return True
        else:
            return False

    def is_legal_k(self, frm: tuple, to: tuple):
        '''
        Проверяет возможность хода короля с позиции frm на позицию to

        :param frm: клетка, с которой пытается пойти короля
        :param to: клетка, на которую пытается попасть короля
        :return: True - если ход возможен, False - если ход невозможен
        '''

        '''проверка на шах при ходе на 1 клетку'''
        if abs(frm[0] - to[0]) < 2 and abs(frm[1] - to[1]) < 2 and \
                not self.is_checked_on_pos(to, self.board[frm[0]][frm[1]].color):
            return True
        '''проверка на рокировку (добавить поле у короля на возможность рокировки)'''
        if abs(frm[0] - to[0]) == 2 and self.is_castling_legal(frm, to):
            self.colorMove = 'white'
            return True
        else:
            return False

    def is_checked_on_pos(self, pos: tuple, king_color: str):
        '''
        Проверка на шах в позиции pos, если бы в ней стоял король цвета king_color

        :param pos: клетка, которую проверяют на шах
        :param king_color: цвет короля, которого проверяют на шах в позиции pos
        :return: True - если шах есть, False - если шаха нет
        '''

        '''проверка на короля противника, около клетки pos'''
        around = [(0, -1), (1, -1), (1, 0), (1, 1),
                  (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for i, j in around:
            if (0 <= pos[0] + i <= 7) and (0 <= pos[1] + j <= 7) and \
                    self.board[pos[0] + i][pos[1] + j].name in ('k', 'K') and \
                    self.board[pos[0] + i][pos[1] + j].color != king_color:
                return True

        '''проверка на шах по j'''
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

        '''проверка на шах по i'''
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

        '''проверка на шах по диагоналям'''
        diag = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        for i_plus, j_plus in diag:
            i = pos[0] + i_plus
            j = pos[1] + j_plus

            '''проверка на шах от пешек'''
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

        '''проверка на шах от коней'''
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1),
                      (2, 1), (1, 2), (-1, 2), (-2, 1)]
        knight_name = 'n' if king_color == 'white' else 'N'
        for i, j in directions:
            if (0 <= pos[0] + i <= 7) and (0 <= pos[1] + j <= 7) and \
                    self.board[pos[0] + i][pos[1] + j].name == knight_name:
                return True

        '''прошли все проверки на шах -> нет шаха'''
        return False

    def is_opened_check(self, frm: tuple, to: tuple, color: str):
        '''
        Проверка на шах, который может возникнуть после хода какой-либо фигурой

        :param frm: позиция, с которой происходит ход фигурой
        :param to: позиция, на которую происходит ход фигурой
        :param color: цвет короля, который проверяется на шах
        :return:
        '''
        board = copy.deepcopy(self)
        board.move(frm, to)
        kingPos = self.whiteKingPos if color == 'white' else self.blackKingPos
        if not board.is_checked_on_pos(kingPos, color):
            return False
        else:
            return True

    def is_castling_legal(self, frm: tuple, to: tuple):
        '''
        Проверка возможности рокировки, при ходе короля с позиции from в позицию to

        :param frm: клетка, с которой король хочет сделать рокировку
        :param to: клетка, на которую король хочет попасть после рокировки
        :return: True - если рокировка возможна, False - если рокировка невозможна
        '''
        kingColor = self.colorMove
        if self.is_checked_on_pos(frm, kingColor):
            return False
        if self.board[frm[0]][frm[1]].did_move:
            return False
        if self.board[frm[0]][frm[1]].color == 'white':
            if frm[0] != 4 and frm[1] != 0:
                return False
            '''(7, 0), (0, 0) - координаты ладей'''
            if to[0] == 6 and to[1] == 0 and self.board[7][0].name == 'R' and \
                    not self.board[7][0].did_move and self.board[5][0].name == '.' and \
                    self.board[6][0].name == '.' and not self.is_checked_on_pos((5, 0), 'white') and \
                    not self.is_checked_on_pos((6, 0), 'white'):
                '''рокировка будет сделана, поэтому переместим ладью сразу из проверки'''
                self.move((7, 0), (5, 0))
                return True
            if to[0] == 2 and to[1] == 0 and self.board[0][0].name == 'R' and \
                    not self.board[0][0].did_move and self.board[3][0].name == '.' and \
                    self.board[2][0].name == '.' and self.board[1][0].name == '.' and \
                    not self.is_checked_on_pos((3, 0), 'white') and \
                    not self.is_checked_on_pos((2, 0), 'white') and \
                    not self.is_checked_on_pos((1, 0), 'white'):
                '''рокировка будет сделана, поэтому переместим ладью сразу из проверки'''
                self.move((0, 0), (3, 0))
                return True
            return False
        else:
            if frm[0] != 4 and frm[1] != 7:
                return False
            '''(7, 7), (0, 7) - координаты ладей'''
            if to[0] == 6 and to[1] == 7 and self.board[7][7].name == 'r' and \
                    not self.board[7][7].did_move and self.board[5][7].name == '.' and \
                    self.board[6][7].name == '.' and not self.is_checked_on_pos((5, 7), 'black') and \
                    not self.is_checked_on_pos((6, 7), 'black'):
                '''рокировка будет сделана, поэтому переместим ладью сразу из проверки'''
                self.move((7, 7), (5, 7))
                return True
            if to[0] == 2 and to[0] == 7 and self.board[0][7].name == 'r' and \
                    not self.board[0][7].did_move and self.board[3][7].name == '.' and \
                    self.board[2][7].name == '.' and self.board[1][7].name == '.' and \
                    not self.is_checked_on_pos((3, 7), 'black') and \
                    not self.is_checked_on_pos((2, 7), 'black') and \
                    not self.is_checked_on_pos((1, 7), 'black'):
                '''рокировка будет сделана, поэтому переместим ладью сразу из проверки'''
                self.move((0, 7), (3, 7))
                return True
            return False

    def is_game_over(self, color: str):
        '''
        Проверка на возможность хода для игрока, играющего за фигуры цвета color

        :param color: цвет стороны, которую проверяют на возможность хода
        :return: False - если партия может продолжаться, 'checkmate' - если сторона color получила мат, 'stalemate' - если на доске стоит пат
        '''
        kingPos = self.whiteKingPos if color == 'white' else self.blackKingPos
        for i in range(8):
            for j in range(8):
                if not self.board[i][j].color == color:
                    continue
                else:
                    '''проверка пешек на возможность ходить'''
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
                    '''проверка коней на возможность ходить'''
                    if self.board[i][j].name in ('n', 'N'):
                        directions = [(-2, -1), (-1, -2), (1, -2),
                                      (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
                        for i_plus, j_plus in directions:
                            if 0 <= i + i_plus <= 7 and 0 <= j + j_plus <= 7 and \
                                    self.is_legal((i, j), (i + i_plus, j + j_plus)):
                                return False
                    '''проверка ладей и ферзя на возможность ходить'''
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
                    '''проверка слонов и ферзя на возможность ходить'''
                    if self.board[i][j].name in ('b', 'B', 'q', 'Q'):
                        diag = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                        for i_plus, j_plus in diag:
                            i_ = i + i_plus
                            j_ = j + j_plus
                            while 0 <= i_ <= 7 and 0 <= j_ <= 7:
                                if self.is_legal((i, j), (i_, j_)):
                                    return False
                                i_ += i_plus
                                j_ += j_plus
                    '''проверка короля на возможность ходить'''
                    if self.board[i][j].name in ('k', 'K'):
                        around = [(0, -1), (1, -1), (1, 0), (1, 1),
                                  (0, 1), (-1, 1), (-1, 0), (-1, -1)]
                        for i_plus, j_plus in around:
                            if 0 <= i + i_plus <= 7 and 0 <= j + j_plus <= 7 and \
                                    self.is_legal((i, j), (i + i_plus, j + j_plus)):
                                return False
        if not self.is_checked_on_pos(kingPos, color):
            return 'stalemate'
        else:
            return 'checkmate'

    def returning_figure(self, frm):
        '''
        Возвращает фигуру на место

        :param frm: клетка, с которой взяли фигуру, и на которую её хотят поставить
        '''
        self.board[frm[0]][frm[1]] = self.board[frm[0]][frm[1]]

    def move(self, frm: tuple, to: tuple):
        '''
        Перемещение фигуры с позиции frm, на позицию to

        :param frm: клетка, с которой ходит фигура
        :param to: клетка, на которую ходит фигура
        '''
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

    def try_move(self, frm: tuple, to: tuple):
        '''
        Попытка сделать ход фигурой с поля frm, на поле to, если это возможно, ход делается функцией move

        :param frm: клетка, с которой ходит фигура
        :param to: клетка, на которую ходит фигура
        :return: если ход возможен, возвращает 'neutral' если партия не закончена, или ('checkmate'/'stalemate', color), где color - проигравшая сторона; возвращает False, если ход невозможен
        '''
        if not self.is_legal(frm, to):
            # print("ILLLEGAL MOVE")
            return False

        self.move(frm, to)
        # print("Move done!!!!!!!!!!!")

        color = self.colorMove
        moveResult = self.is_game_over(color)
        if moveResult:
            return (moveResult, color)
        else:
            return 'neutral'

        return True

    def serialize(self) -> LiteralString:
        '''Функция конвертации данного объекта в json.
        Всеми параметрами, кроме расположения шахмат, пренебрегает

        :return: json строка доски'''
        res = '{"board": ['
        for i in range(8):
            res += '['
            for j in range(8):
                ser = self.board[i][j].serialize()
                res += ser + (',' if j != 7 else '')

            res += ']' + (',' if i != 7 else '')
        res += ']}'
        return res

    def deserialize(data):
        '''Функция конвертации json строки в ``Board``

        :rtype: Board
        :return: ``Board`` из json строки'''
        board = data['board']
        res = Board()

        for i in range(8):
            for j in range(8):
                figure = Figure.Figure.deserialize(board[i][j])
                res.board[i][j] = figure

        return res
