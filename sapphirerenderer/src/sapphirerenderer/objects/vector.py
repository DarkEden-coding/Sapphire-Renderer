from ..object_classes.flat_faces_object import FlatFacesObject
import numpy as np


def average_points(points):
    """
    Get the average of a list of points
    :param points: list of points
    :return: average point
    """
    return np.mean(points, axis=0)


class Vector(FlatFacesObject):
    def __init__(
        self,
        start_point=np.array([0.0, 0.0, 0.0]),
        vector_components=np.array([1.0, 1.0, 1.0]),
        color=(0, 0, 0),
        thickness=0.02,
    ):
        """
        Vector object
        :param start_point: the start point of the vector
        :param vector_components: the direction and length of the vector
        :param color: the color of the vector
        :param thickness: the thickness of the vector
        """
        start_point = 0.5 * np.array(start_point)

        self.start_point = start_point
        self.vector_components = vector_components
        self.end_point = start_point + vector_components
        self.thickness = thickness
        self.color = color

        direction = vector_components / np.linalg.norm(vector_components)
        vertices, faces = self.create_faces(
            self.start_point, self.end_point, direction, thickness, color
        )

        super().__init__(
            vertices=vertices,
            faces=faces,
            color=color,
            compile_verts=True,
            position=start_point,
            move_to_zero=False,
        )

    def get_start_point(self):
        # calculate the start point of the vector based on vertices
        return average_points(self.vertices[:4])

    def get_end_point(self):
        # calculate the end point of the vector based on vertices
        return average_points(self.vertices[4:8])

    def create_faces(self, start, end, direction, thickness, color):
        # Define the vertices and faces
        perpendicular_vector = np.cross(direction, np.array([1, 0, 0]))
        if (
            np.linalg.norm(perpendicular_vector) < 1e-6
        ):  # direction was collinear with x-axis
            perpendicular_vector = np.cross(direction, np.array([0, 1, 0]))

        perpendicular_vector = (
            perpendicular_vector / np.linalg.norm(perpendicular_vector) * thickness
        )
        perpendicular_vector2 = np.cross(direction, perpendicular_vector)
        perpendicular_vector2 = (
            perpendicular_vector2 / np.linalg.norm(perpendicular_vector2) * thickness
        )

        vertices = np.array(
            [
                start + perpendicular_vector,
                start - perpendicular_vector,
                start + perpendicular_vector2,
                start - perpendicular_vector2,
                end + perpendicular_vector,
                end - perpendicular_vector,
                end + perpendicular_vector2,
                end - perpendicular_vector2,
            ]
        )

        faces = [
            ([0, 1, 5, 4], color),  # Face 1
            ([2, 3, 7, 6], color),  # Face 2
        ]

        return vertices.tolist(), faces
