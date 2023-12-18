from typing import *

class Vector2:
    '''
    Класс, реализующий базовые операции над веторами, такие как сложение, вычитание,
    умножение на число и др.
    '''

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        '''Координата x'''
        self.y: float = y
        '''Координата y'''

    def __add__(self, v):
        '''Операция сложения двух векторов
        
        :param v: второй слагаемый вектор
        :type v: Vector2
        :rtype: Vector2
        :return: результат покомпонентного сложения векторов'''
        x = self.x + v.x
        y = self.y + v.y
        return Vector2(x, y)

    def __sub__(self, v):
        '''Операция разности двух векторов
        
        :param v: вычитаемый вектор
        :type v: Vector2
        :rtype: Vector2
        :return: результат покомпонентного вычитания векторов'''
 
        x = self.x - v.x
        y = self.y - v.y
        return Vector2(x, y)

    def __mul__(self, n: float):
        '''Операция умножения вектора на число
        
        :param n: коэффициент умножения
        :rtype: Vector2
        :return: результат покомпонентного умножения вектора на число'''
        x = self.x * n
        y = self.y * n
        return Vector2(x, y)

    def __truediv__(self, n):
        '''Операция деления вектора на число
        
        :param n: делитель вектора
        :rtype: Vector2
        :return: результат покомпонентного деления вектора на число'''
        x = self.x / n
        y = self.y / n
        return Vector2(x, y)

    def __neg__(self):
        '''Операция отрицания вектора
        
        :rtype: Vector2
        :return: результат покомпонентного отрицания вектора'''
        x = -self.x
        y = -self.y
        return Vector2(x, y)

    def __str__(self) -> LiteralString:
        '''Операция перевода типа ``Vector2`` в строку
        
        :return: строка из ``Vector2``'''
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, v) -> bool:
        '''Операция покомпонентного сравнения двух векторов
        
        :param v: вектор, с которым сравнивается данный
        :type v: Vector2
        :return: результат сравнения двух векторов'''
        return self.x == v.x and self.y == v.y

    def length(self) -> float:
        '''Длинна данного вектора'''
        return (self.x ** 2 + self.y ** 2) ** (1/2)

    def to_tuple(self) -> Tuple[float, float]:
        '''
        :return: ``Vector2``, переведенный в кортеж
        '''
        return (self.x, self.y)


def from_tuple(t: Tuple[float, float]) -> Vector2:
    '''
    :param t: кортеж, который надо перевести в Vector2
    :return: ``Vector2``, переведенный из данного кортежа
    '''
    return Vector2(t[0], t[1])
