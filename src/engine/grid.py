from .vector2 import Vector2
from . import game_object
from typing import *


def find_closest(grid, point: Vector2) -> Vector2:
    '''
    Ищет ближайщую к заданной точке клетку сетки.

    :param grid: сетка, относительно которой производится поиск.
    :type grid: Grid
    :param point: точка, относитльно который ищется ближайшая клетка сетки *grid*
    :return: относительная координата клетки в сетке, располагаеющейся ближе всего к заданной точке.
    '''
    pts = grid.get_points()
    res = Vector2(0, 0)

    for i in range(len(pts)):
        for j in range(len(pts[0])):
            new_point = pts[i][j]
            cur_point = pts[res.x][res.y]
            cur = cur_point - point
            new = new_point - point
            if cur.length() > new.length():
                res = Vector2(i, j)

    return res


class Grid:
    '''
    Компонент сетки. Располагает каждую собственную точку на
    равном расстоянии от соседних. По вертикали и по горизонтали расстояния могут
    различаться.
    '''

    def init(self, go, size, capacity) -> None:
        '''
        Инициализатор. Аналогичен __init__. 
        Все параметры соответствуют полям класса.

        :raises ValueError: если размеры сетки отрицательные значения
        '''
        self.go: game_object.GameObject = go
        '''``GameObject``, к которому прикреплен данный компонент.'''

        check_size = size.x >= 0 and size.y >= 0
        if not check_size:
            raise ValueError

        self.size: Vector2 = size
        '''Размер сетки в пикселях.'''
        self.capacity: Vector2 = capacity
        '''Количество точек по горизонтали и по вертикали.'''

    def update(self) -> None:
        '''Пустой метод кадра компонента.'''
        pass

    def get_points(self) -> List[List[Vector2]]:
        '''
        Возвращает список абсолютных координат точек сетки.

        :return: список абсолютных координат точек сетки. 
        '''
        size = self.size
        cap = self.capacity
        pos = self.go.position

        distX = size.x / (cap.x - 1)
        distY = size.y / (cap.y - 1)

        points = [[0] * cap.y for _ in range(cap.x)]
        for i in range(cap.x):
            for j in range(cap.y):
                offset = Vector2(i * distX, j * distY)
                points[i][j] = pos + offset

        return points


class GridBinder:
    '''Компонент, отвечающий за прикрепление ``GameObject`` к 
    определенной точке ``Grid``'''
    def init(self, go: game_object.GameObject, grd: Grid, coord: Vector2, instant_bind: bool=True) -> None:
        '''
        Инициализатор. Аналогичен __init__. Каждый параметр соответствует полю класса.
        '''
        self.grd: Grid= grd
        '''``Grid``, относительно которого будет проводиться закрепление'''
        self.coord: Vector2 = coord
        '''Относительная точка ``Grid``, к которой будет прикреплен объект.'''
        self.go: game_object.GameObject = go
        '''``GameObject`` к которому прикреплен компонент.'''
        self.binded: bool = instant_bind
        '''Состояние, показывающее, должна ли быть закреплена точка в данный момент.'''

    def update(self) -> None:
        '''Метод кадра компонента.'''
        if not self.binded:
            return

        self.__bind()

    def __bind(self) -> None:
        '''
        Закрытый метод класса, перемещающий объект к точке закрепления.
        '''
        points = self.grd.get_points()
        x, y = self.coord.to_tuple()

        self.go.position = points[x][y]
