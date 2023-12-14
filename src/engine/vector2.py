class Vector2:
    '''
    Class that implement basic functions over 2-dimensional vectors
    like add, substract and others.

    :param float x: sets x coordinate of a vector
    :param float y: sets y coordinate of a vector
    '''

    def __init__(self, x, y):
        self.x = x
        '''x coordinate'''
        self.y = y
        '''y coordinate'''

    def __add__(self, v):
        x = self.x + v.x
        y = self.y + v.y
        return Vector2(x, y)

    def __sub__(self, v):
        x = self.x - v.x
        y = self.y - v.y
        return Vector2(x, y)

    def __mul__(self, n):
        x = self.x * n
        y = self.y * n
        return Vector2(x, y)

    def __truediv__(self, n):
        x = self.x / n
        y = self.y / n
        return Vector2(x, y)

    def __neg__(self):
        x = -self.x
        y = -self.y
        return Vector2(x, y)

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** (1/2)

    def to_tuple(self):
        '''
        :rtype: tuple[float, float]
        :return: tuple that converted from Vector2
        '''
        return (self.x, self.y)


def from_tuple(t):
    '''
    :param tuple[float, float] t: convertion tuple 
    :rtype: Vector2
    :return: Vector2 that converted from tuple
    '''
    return Vector2(t[0], t[1])
