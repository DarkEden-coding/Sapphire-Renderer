from ..object_classes.wireframe_object import WireframeObject
import numpy as np


class Cuboid(WireframeObject):
    def __init__(
        self,
        bottom_corner=np.array([0, 0, 0]),
        top_corner=np.array([1, 1, 1]),
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
    ):
        self.top_corner = top_corner
        self.bottom_corner = bottom_corner

        vertices = np.array(
            [
                np.array([bottom_corner[0], bottom_corner[1], bottom_corner[2]]),
                np.array([top_corner[0], bottom_corner[1], bottom_corner[2]]),
                np.array([top_corner[0], top_corner[1], bottom_corner[2]]),
                np.array([bottom_corner[0], top_corner[1], bottom_corner[2]]),
                np.array([bottom_corner[0], bottom_corner[1], top_corner[2]]),
                np.array([top_corner[0], bottom_corner[1], top_corner[2]]),
                np.array([top_corner[0], top_corner[1], top_corner[2]]),
                np.array([bottom_corner[0], top_corner[1], top_corner[2]]),
            ]
        )

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

    def check_collision(self, point):
        # use vertices not corners to check collision
        return (
            self.vertices[0][0] <= point[0] <= self.vertices[1][0]
            and self.vertices[0][1] <= point[1] <= self.vertices[2][1]
            and self.vertices[0][2] <= point[2] <= self.vertices[4][2]
        )
