class Scene:
    '''
    Scene stores objects that are currently present
    and activates their functionality.

    :param list[GameObject] objects: sets *objects* field
    '''

    def __init__(self, objects):
        self.objects = objects
        '''List of objects that are present in scene'''

    def update(self):
        '''
        Method that invokes update of every game object's component
        '''
        for obj in self.objects:
            for comp in obj.components:
                comp.update()
