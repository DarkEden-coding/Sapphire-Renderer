from ..object_classes.wireframe_object import WireframeObject
import numpy as np


class Axes(WireframeObject):
    def __init__(self, position=np.array([0.0, 0.0, 0.0]), color=(0, 0, 0)):
        vertices = np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ],
            dtype=float,
        )

        lines = [
            [0, 1, (159, 0, 0)],
            [0, 2, (0, 159, 0)],
            [0, 3, (0, 0, 159)],
        ]

        super().__init__(vertices, lines, position, color)
