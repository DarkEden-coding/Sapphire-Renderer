from ..object_classes.flat_faces_object import FlatFacesObject
import numpy as np


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

    def update_vector(self, start_point=None, vector_components=None):
        """
        Update the vector
        :param start_point: the start point of the vector
        :param vector_components: the direction and length of the vector
        """
        if start_point is not None:
            start_point = 0.5 * np.array(start_point)
            self.start_point = start_point

        if vector_components is not None:
            self.vector_components = vector_components

        self.end_point = self.start_point + self.vector_components

        direction = vector_components / np.linalg.norm(vector_components)
        vertices, faces = self.create_faces(
            self.start_point, self.end_point, direction, self.thickness, self.color
        )

        self.faces = faces
        self.vertices = vertices


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
