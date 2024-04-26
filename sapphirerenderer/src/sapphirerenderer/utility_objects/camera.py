import numpy as np
from ..point_math.matricies import get_pitch_yaw_matrix


class Camera:
    def __init__(
        self,
        renderer,
        position=np.array([0.0, 0.0, 0.0]),
        rotation=np.array((0.0, 0.0)),
        fov=80,
    ):
        self.position = position
        self.rotation = rotation
        self.fov = fov
        self.rotation_matrix = self.get_rotation_matrix()
        self.size = np.array((renderer.width, renderer.height))
        self.offset_array = np.array([self.size[0] / 2, self.size[1] / 2])
        self.focal_length = (self.size[0] / 2) / np.tan((self.fov / 2) * (np.pi / 180))

        # compute the field of view
        self.fov_side = np.arctan(self.size[0] / (2 * self.focal_length)) + 0.5
        self.fov_top = np.arctan(self.size[1] / (2 * self.focal_length)) + 0.5

    def move_absolute(self, position):
        position = np.array([-position[1], position[0], position[2]])
        self.position = position

    def move_relative(self, position):
        position = np.array([-position[1], position[0], position[2]])
        self.position += position @ self.rotation_matrix

    def rotate_absolute(self, rotation):
        self.rotation = rotation

    def rotate_relative(self, rotation):
        self.rotation += rotation

    def update(self):
        self.rotation_matrix = self.get_rotation_matrix()

    def get_rotation_matrix(self):
        return get_pitch_yaw_matrix(*self.rotation)
