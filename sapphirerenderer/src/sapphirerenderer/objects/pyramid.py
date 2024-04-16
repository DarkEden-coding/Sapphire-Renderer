import numpy as np
from ..object_classes.wireframe_object import WireframeObject


def generate_pyramid_points_and_segments(base_side_length, height):
    # Define the base vertices
    base_vertices = np.array(
        [
            [-base_side_length / 2, -base_side_length / 2, 0],
            [-base_side_length / 2, base_side_length / 2, 0],
            [base_side_length / 2, base_side_length / 2, 0],
            [base_side_length / 2, -base_side_length / 2, 0],
        ]
    )

    # Define the apex vertex
    apex_vertex = np.array([0, 0, height])

    # Combine vertices
    vertices = np.vstack((base_vertices, apex_vertex))

    # Define base lines
    base_lines = [[0, 1], [1, 2], [2, 3], [3, 0]]

    # Define lines from apex to base vertices
    apex_lines = [[4, i] for i in range(4)]

    # Combine lines
    lines = np.vstack((base_lines, apex_lines))

    return vertices, lines


class Pyramid(WireframeObject):
    def __init__(
        self,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        base_side_length=1.0,
        height=1.0,
    ):
        vertices, lines = generate_pyramid_points_and_segments(base_side_length, height)
        super().__init__(vertices, lines, position, color)
