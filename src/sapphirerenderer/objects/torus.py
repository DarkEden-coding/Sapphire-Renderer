import numpy as np
from ..object_classes.vert_line_object import VertLineObject


def generate_torus_points_and_segments(radius_major, radius_minor, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)

    x = (radius_major + radius_minor * np.cos(V)) * np.cos(U)
    y = (radius_major + radius_minor * np.cos(V)) * np.sin(U)
    z = radius_minor * np.sin(V)

    points = np.stack((x.flatten(), y.flatten(), z.flatten()), axis=-1)

    # Generate line segments
    segments = []
    for i in range(resolution):
        for j in range(resolution):
            index = i * resolution + j
            if j < resolution - 1:
                segments.append([index, index + 1])
            else:
                segments.append([index, i * resolution])

            if i < resolution - 1:
                segments.append([index, index + resolution])
            else:
                segments.append([index, j])

    return points, np.array(segments)


class Torus(VertLineObject):
    def __init__(self, position=np.array([0.0, 0.0, 0.0]), color=(0, 0, 0)):
        vertices, lines = generate_torus_points_and_segments(2, 0.3, 20)

        super().__init__(vertices, lines, position, color)
