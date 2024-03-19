import numpy as np
from numba import njit


@njit(fastmath=True)
def project_point(point, offset_array, focal_length):
    if point[1] < 0:
        return None, 1

    focal_length_divided_by_y = focal_length / point[1]

    projected_point = np.array(
        [
            point[0] * focal_length_divided_by_y,
            -point[2] * focal_length_divided_by_y,
        ]
    )

    projected_point += offset_array

    scale_factor = 1 / np.linalg.norm(point)

    return projected_point, scale_factor
