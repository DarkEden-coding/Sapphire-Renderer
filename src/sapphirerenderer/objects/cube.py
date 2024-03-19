from ..object_classes.vert_line_object import VertLineObject
import numpy as np


class Cube(VertLineObject):
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

        lines = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
        ]

        super().__init__(vertices, lines, position, color)

        self.move_relative(np.array([-size / 2, -size / 2, -size / 2]))
