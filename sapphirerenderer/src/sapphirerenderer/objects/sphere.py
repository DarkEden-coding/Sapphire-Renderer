import numpy as np
from ..object_classes.wireframe_object import WireframeObject


def generate_sphere_points_and_segments(radius, resolution):
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    THETA, PHI = np.meshgrid(theta, phi)

    x = radius * np.sin(THETA) * np.cos(PHI)
    y = radius * np.sin(THETA) * np.sin(PHI)
    z = radius * np.cos(THETA)

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


class Sphere(WireframeObject):
    def __init__(
        self,
        radius=1.0,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        resolution=20,
    ):
        vertices, lines = generate_sphere_points_and_segments(radius, resolution)
        super().__init__(vertices, lines, position, color)
