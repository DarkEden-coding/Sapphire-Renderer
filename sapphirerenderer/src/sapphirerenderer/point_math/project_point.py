import numpy as np
from numba import njit


@njit(fastmath=True)
def project_point(point, offset_array, focal_length, screen_size, fov_side, fov_top):
    if point[1] <= 0:
        return None, 1

    # if point is out of view, return None
    top_angle = np.arctan2(point[2], point[1])
    side_angle = np.arctan2(point[0], point[1])

    if abs(top_angle) > fov_top or abs(side_angle) > fov_side:
        return None, 1

    focal_length_divided_by_y = focal_length / point[1]

    projected_point = np.array(
        [
            point[0] * focal_length_divided_by_y,
            -point[2] * focal_length_divided_by_y,
        ]
    )

    projected_point += offset_array

    # if the point is more than 2000 pixels off the edge of the screen, return None
    if (
        abs(projected_point[0]) > screen_size[0] + 2000
        or abs(projected_point[1]) > screen_size[1] + 2000
    ):
        return None, 1

    point_size = 1 / np.linalg.norm(point)

    return projected_point, point_size
