import numpy as np
from ..object_classes.flat_faces_object import FlatFacesObject


def generate_sphere_faces(radius, resolution):
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    THETA, PHI = np.meshgrid(theta, phi)

    x = radius * np.sin(THETA) * np.cos(PHI)
    y = radius * np.sin(THETA) * np.sin(PHI)
    z = radius * np.cos(THETA)

    vertices = np.stack((x.flatten(), y.flatten(), z.flatten()), axis=-1)

    faces = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            index = i * resolution + j
            faces.append(
                (
                    [index, index + 1, index + resolution + 1, index + resolution],
                    (255, 111, 100),
                )
            )

    # Connect the last row with the first one to close the sphere
    for j in range(resolution - 1):
        index = (resolution - 1) * resolution + j
        faces.append(([index, index + 1, j + 1, j], (255, 111, 100)))

    return vertices, faces


class Fsphere(FlatFacesObject):
    def __init__(
        self,
        radius=1.0,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        resolution=20,
    ):
        vertices, faces = generate_sphere_faces(radius, resolution)
        super().__init__(vertices, faces, position, color)
