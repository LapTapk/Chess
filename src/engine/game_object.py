from vector2 import Vector2


class GameObject:
    '''
    An entity, whose behaviour is defined by set of ``components``. Also contains
    a position, rotation and scale in pygame plane.

    :param Vector2 pos: sets *position* field
    :param float rot: sets *rotation* field
    :param Vector2 scale: sets *scale* field
    :param list components: sets *components* field
    '''

    def __init__(self, pos=Vector2(0, 0), rot=0, scale=Vector2(1, 1), components=[]):
        self.position = pos
        '''Position of an object'''
        self.rotation = rot
        '''Rotation of an object'''
        self.scale = scale
        '''Scale of an object'''

        self.components = components
        '''``Components`` of an object'''
        for comp in self.components:
            comp.go = self

    def get_component(self, type):
        '''
        Method that returns first occurrence of ``component`` of certain *type*

        :param _ClassInfo type: type of a ``component`` to search 
        :rtype: *type* or None
        :return: first ``component`` of *type* or None, if it does not exist 
        '''
        for comp in self.components:
            if isinstance(comp, type):
                return comp

        return None
