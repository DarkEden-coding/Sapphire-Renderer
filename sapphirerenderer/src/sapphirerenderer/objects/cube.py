from ..object_classes.wireframe_object import WireframeObject
import numpy as np


class Cube(WireframeObject):
    def __init__(self, position=np.array([0.0, 0.0, 0.0]), color=(0, 0, 0), size=1):
        vertices = np.array(
            [
                np.array([0, 0, 0]),
                np.array([size, 0, 0]),
                np.array([size, size, 0]),
                np.array([0, size, 0]),
                np.array([0, 0, size]),
                np.array([size, 0, size]),
                np.array([size, size, size]),
                np.array([0, size, size]),
            ],
            dtype=float,
        )

        faces = [
            ([0, 1, 2, 3], (255, 111, 100)),
            ([4, 5, 6, 7], (255, 111, 65)),
            ([0, 1, 5, 4], (255, 65, 100)),
            ([1, 2, 6, 5], (65, 111, 100)),
            ([2, 3, 7, 6], (255, 189, 100)),
            ([3, 0, 4, 7], (255, 111, 200)),
        ]

        lines = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

        super().__init__(vertices, lines, position, color)

        self.move_relative(np.array([-size / 2, -size / 2, -size / 2]))
