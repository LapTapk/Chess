import unittest
from . import Board


class BoardTest(unittest.TestCase):
    '''Тесты'''

    '''Тесты начальных позиций'''
    def test1(self):
        board = Board.Board()
        board.startPosition()
        self.assertEqual(board.is_legal((0, 0), (0, 7)), False)

    def test2(self):
        board = Board.Board()
        board.startPosition()
        self.assertEqual(board.is_legal((6, 0), (5, 2)), True)

    '''Тест связки'''
    def test3(self):
        board = Board.Board()
        figures = [((4, 1), 'K'), ((6, 0), 'k'), ((0, 0), 'R'), ((5, 0), 'n')]
        board.createPosition(figures)
        self.assertEqual(board.is_legal((5, 0), (4, 2)), False)

    '''Король под шахом'''
    def test4(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        board.move((5, 2), (5, 6))
        self.assertEqual(board.is_legal((0, 6), (0, 5)), False)

    def test5(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        board.move((5, 2), (5, 6))
        self.assertEqual(board.is_legal((4, 7), (5, 6)), True)

    '''Проверка на конец игры'''

    '''Проверка на мат'''
    def test6(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((5, 0), (2, 3))
        board.move((1, 7), (2, 5))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        board.move((5, 2), (5, 6))
        self.assertEqual(board.is_game_over('black'), 'checkmate')

    def test7(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((5, 0), (2, 3))
        board.move((1, 7), (2, 5))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        self.assertEqual(board.is_game_over('white'), False)

    '''Проверка на пат'''
    def test8(self):
        board = Board.Board()
        figures = [((2, 0), 'K'), ((0, 0), 'k'), ((1, 2), 'Q')]
        board.createPosition(figures)
        self.assertEqual(board.is_game_over('black'), 'stalemate')

    def test9(self):
        board = Board.Board()
        figures = [((2, 0), 'K'), ((0, 0), 'k'), ((1, 2), 'Q')]
        board.createPosition(figures)
        self.assertEqual(board.is_game_over('white'), False)


    '''Проверка рокировки'''
    def test10(self):
        board = Board.Board()
        figures = [((4, 0), 'K'), ((4, 7), 'k'), ((0, 0), 'R'), ((0, 7), 'r')]
        board.createPosition(figures)
        self.assertEqual(board.is_castling_legal((4, 0), (2, 0)), True)

    def test11(self):
        board = Board.Board()
        figures = [((4, 0), 'K'), ((4, 7), 'k'), ((0, 0), 'R'), ((0, 7), 'r')]
        board.createPosition(figures)
        board.try_move((4, 0), (2, 0))
        self.assertEqual(board.is_castling_legal((4, 7), (2, 7)), False)

    '''Проверка взятия на проходе'''
    def test12(self):
        board = Board.Board()
        figures = [((4, 0), 'K'), ((4, 7), 'k'), ((5, 4), 'P'), ((4, 6), 'p')]
        board.createPosition(figures)
        board.move((4, 6), (4, 4))
        board.colorMove = 'white'
        self.assertEqual(board.is_legal((5, 4), (4, 5)), True)

    'Проверка полей на шах'
    def test13(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((5, 0), (2, 3))
        board.move((1, 7), (2, 5))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        board.showBoardConsole()
        self.assertEqual(board.is_checked_on_pos((7, 3), 'white'), True)

    def test14(self):
        board = Board.Board()
        board.startPosition()
        board.move((4, 1), (4, 3))
        board.move((4, 6), (4, 4))
        board.move((5, 0), (2, 3))
        board.move((1, 7), (2, 5))
        board.move((3, 0), (5, 2))
        board.move((3, 6), (3, 5))
        board.showBoardConsole()
        self.assertEqual(board.is_checked_on_pos((4, 0), 'white'), False)

    '''Проверка на вскрытый шах про своём ходе'''
    def test15(self):
        board = Board.Board()
        figures = [((4, 1), 'K'), ((6, 0), 'k'), ((0, 0), 'R'), ((5, 0), 'n')]
        board.createPosition(figures)
        board.blackKingPos = (6, 0)
        board.whiteKingPos = (4, 1)
        self.assertEqual(board.is_opened_check((5, 0), (4, 2), 'black'), True)

    def test16(self):
        board = Board.Board()
        figures = [((4, 1), 'K'), ((6, 0), 'k'), ((0, 0), 'R'), ((5, 0), 'n')]
        board.createPosition(figures)
        board.blackKingPos = (6, 0)
        board.whiteKingPos = (4, 1)
        self.assertEqual(board.is_opened_check((0, 0), (5, 0), 'white'), False)


