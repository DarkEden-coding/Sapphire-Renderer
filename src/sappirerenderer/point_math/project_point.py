from utility_objects.camera import Camera
import numpy as np


def project_point(point, camera: Camera):
    """
    Project a 3D point to 2D space using a camera
    :param point: the 3D point to project in np.array([x, y, z])
    :param camera: the camera object to project with
    :return: np.array([x, y]) the 2D point
    """
    camera_matrix = camera.rotation_matrix

    rotated_point = camera_matrix @ (point - camera.position)

    projected_point = np.array(
        [
            (rotated_point[0] * camera.focal_length) / rotated_point[1],
            (rotated_point[2] * camera.focal_length) / rotated_point[1],
        ]
    )

    if rotated_point[1] < 0:
        return None, 1

    scale_factor = 1 / np.sqrt(
        rotated_point[0] ** 2 + rotated_point[1] ** 2 + rotated_point[2] ** 2
    )

    return (
        projected_point + np.array([camera.size[0] / 2, camera.size[1] / 2]),
        scale_factor,
    )
