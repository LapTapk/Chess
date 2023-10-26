from engine.vector2 import Vector2


class Grid:
    '''
    Grid ``component`` stores data about *grid* and helps
    to find absolute coordinates of *grid's* points. *Grid* is a set 
    of points and it has rectangular shape.

    :param Vector2 size: sets *size* field
    :param Vector2 capacity: sets *capacity* field
    '''

    def __init__(self, size, capacity):
        self.go = None
        '''Game object renderer is attached to'''

        check_size = size.x >= 0 and size.y >= 0
        if not check_size:
            raise ValueError

        self.size = size
        '''Size of a grid in pixels'''
        self.capacity = capacity
        '''Capacity of point that are in a grid'''

    def update(self):
        '''
        ``Component's`` method is empty
        '''
        pass

    def get_points(self):
        '''
        :rtype: list[Vector2]
        :return: Set of absolute points that are in this rectangular *grid*
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


class GridBind:
    '''
    ``Component`` that attaches it's ``game object`` to some point
    of the ``grid``

    :param GridByCapacity grid: sets *grid* field
    :param Vector2 coord: sets *coord* field
    :param bool instant_bind=True: tells if ``game object`` should bind right \
    after creation of the ``grid bind's`` instance
    '''

    def __init__(self, grid, coord, instant_bind=True):
        self.grid = grid
        '''``Grid`` which point will be anchor for ``game object``'''
        self.coord = coord
        '''Local coordinate of ``grid's`` point'''
        self.go = None
        '''``Game object`` that ``component`` is attached to'''
        self.binded = instant_bind
        '''Tells if ``game object`` should be binded'''

    def update(self):
        '''``Component`` method. Binds if need to'''
        if not self.binded:
            return

        self.bind()

    def bind(self):
        '''Sets position of *game object* to anchor from *grid*'''
        points = self.grid.get_points()
        x, y = self.coord.to_tuple()

        self.go.position = points[x][y]
