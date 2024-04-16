from ..object_classes.wireframe_object import WireframeObject
import numpy as np


class Line(WireframeObject):
    def __init__(self, position=np.array([0.0, 0.0, 0.0]), color=(0, 0, 0)):
        vertices = np.array(
            [
                [0, 0, 0],
                [0, 0, 0],
            ],
            dtype=float,
        )

        lines = [[0, 1, color]]

        super().__init__(vertices, lines, position, color)

    def change_color(self, color):
        self.lines[0][2] = color
        self.color = color

    def change_vertices(self, vertices):
        self.vertices = vertices

    def change_start(self, start):
        self.vertices[0] = start

    def change_end(self, end):
        self.vertices[1] = end
