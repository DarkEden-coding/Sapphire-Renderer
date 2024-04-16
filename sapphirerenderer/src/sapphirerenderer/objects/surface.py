from ..object_classes.surface_object import SurfaceObject


class Surface(SurfaceObject):
    def __init__(self, vertices, color=(0, 0, 0)):
        super().__init__(vertices, color=color)
