import unittest
from . import Figure
from . import Board


class BoardTest(unittest.TestCase):

    '''Проверка изменения имён взависимости от цвета фигуры'''
    def test1(self):
        fig = Figure.Figure('white', (0, 0))
        fig.name = 'k'
        self.assertEqual(fig.registerFromColor(), 'K')

    def test2(self):
        fig = Figure.King('black', (0, 0))
        fig.name = 'k'
        self.assertEqual(fig.registerFromColor(), 'k')

    def test3(self):
        fig = Figure.Rock('white', (0, 0))
        self.assertEqual(fig.showFigureConsole(), 'R')
    