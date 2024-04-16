import numpy as np
from ..object_classes.wireframe_object import WireframeObject


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


class Torus(WireframeObject):
    def __init__(
        self,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        radius_major=1.5,
        radius_minor=0.5,
        resolution=20,
    ):
        vertices, lines = generate_torus_points_and_segments(
            radius_major, radius_minor, resolution
        )
        self.radius_major = radius_major
        self.radius_minor = radius_minor
        self.resolution = resolution
        self.position = position
        self.color = color

        super().__init__(vertices, lines, position, color)

    def copy(self):
        return Torus(
            position=self.position,
            color=self.color,
            radius_major=1.5,
            radius_minor=0.5,
            resolution=20,
        )
