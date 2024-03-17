import numpy as np
from numba import njit


@njit(fastmath=True)
def project_point(point, rotation_matrix, camera_position, camera_size, focal_length):
    rotated_point = rotation_matrix @ (point - camera_position)
    y_rotated = rotated_point[1]

    if y_rotated < 0:
        return None, 1

    focal_length_divided_by_y = focal_length / y_rotated

    projected_point = np.array([
        rotated_point[0] * focal_length_divided_by_y,
        -rotated_point[2] * focal_length_divided_by_y,
    ])

    offset_x = camera_size[0] / 2
    offset_y = camera_size[1] / 2

    offset_array = np.array([offset_x, offset_y])

    projected_point += offset_array

    scale_factor = 1 / np.linalg.norm(rotated_point)

    return projected_point, scale_factor
