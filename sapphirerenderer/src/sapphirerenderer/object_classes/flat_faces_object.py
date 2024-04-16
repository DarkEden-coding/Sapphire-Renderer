from ..object_classes.base_object import Object
import pygame
from ..point_math.average_points import average_points
import numpy as np
from ..point_math.project_point import project_point
from ..point_math.matricies import get_pitch_yaw_roll_matrix
from numba import njit

pygame.init()


@njit(fastmath=True)
def get_vertex_distances(vertices, camera_position):
    return [np.linalg.norm(vertex - camera_position) for vertex in vertices]


def get_face_distances(faces, vertices, camera_position):
    vertex_distances = get_vertex_distances(vertices, camera_position)
    face_distances = []
    for face in faces:
        face_distance = 0
        for vertex_index in face[0]:
            face_distance += vertex_distances[vertex_index]
        face_distances.append(face_distance / len(face[0]))
    return face_distances


class FlatFacesObject(Object):
    def __init__(
        self,
        vertices,
        faces,
        position=np.array([0, 0, 0]),
        color=(0, 0, 0),
        shadow=False,
        shadow_effect=1,
    ):
        """
        Object with flat faces
        :param vertices: the vertices of the object
        :param faces: the faces of the object
        :param position: the position of the object
        :param color: the color of the object
        :param shadow: whether to render shadows
        :param shadow_effect: the strength of the shadow
        """
        self.original_vertices = vertices.copy()
        self.center_point = average_points(vertices)
        self.position = position
        self.shadow_effect = shadow_effect

        super().__init__(color=color, position=self.position)
        self.vertices = vertices
        self.faces = faces
        self.rotation = np.array([0, 0, 0], dtype=float)
        self.shadow = shadow
        self.negative_rotation_matrix = get_pitch_yaw_roll_matrix(*-self.rotation)

        self.drawing = False
        self.ambiguous = False

        self.move_absolute(position)

        self.show()

    def move_relative(self, vector):
        """
        Move the object by a relative amount
        :param vector: the amount to move by
        :return:
        """
        self._wait_for_draw()

        self.ambiguous = True
        self.position += vector
        for i in range(len(self.vertices)):
            self.vertices[i] += vector
        self.center_point = average_points(self.vertices)
        self.ambiguous = False

    def move_absolute(self, vector):
        """
        Move the object to an absolute position
        :param vector: the position to move to
        :return:
        """
        self._wait_for_draw()

        self.ambiguous = True
        vector = np.array(vector, dtype=float)
        self.position = vector
        for i in range(len(self.vertices)):
            self.vertices[i] = self.original_vertices[i] + vector
        self.center_point = average_points(self.vertices)
        self.ambiguous = False

    def __rotate(self, x_axis, y_axis, z_axis):
        self._wait_for_draw()

        self.ambiguous = True
        rotation_matrix = get_pitch_yaw_roll_matrix(x_axis, z_axis, y_axis)
        self.vertices = np.dot(self.vertices, rotation_matrix.T)
        self.original_vertices = np.dot(self.original_vertices, rotation_matrix.T)
        self.rotation += np.array([x_axis, z_axis, y_axis], dtype=float)
        self.negative_rotation_matrix = get_pitch_yaw_roll_matrix(*-self.rotation)
        self.ambiguous = False

    def rotate_local(self, x_axis, y_axis, z_axis):
        """
        Rotate the object around its center point
        :param x_axis: x axis rotation in degrees
        :param y_axis: y axis rotation in degrees
        :param z_axis: z axis rotation in degrees
        :return:
        """
        # convert to radians
        x_axis, y_axis, z_axis = (
            np.radians(x_axis),
            np.radians(y_axis),
            np.radians(z_axis),
        )

        self._wait_for_draw()
        self.ambiguous = True
        self.vertices -= self.center_point
        self.__rotate(x_axis, y_axis, z_axis)
        self.vertices += self.center_point
        self.ambiguous = False

    def rotate_around_point(
        self, x_axis, y_axis, z_axis, point=np.array([0, 0, 0], dtype=float)
    ):
        """
        Rotate the object around a point
        :param x_axis: x axis rotation in degrees
        :param y_axis: y axis rotation in degrees
        :param z_axis: z axis rotation in degrees
        :param point: the point to rotate around
        :return:
        """

        # convert to radians
        x_axis, y_axis, z_axis = (
            np.radians(x_axis),
            np.radians(y_axis),
            np.radians(z_axis),
        )

        self._wait_for_draw()

        self.ambiguous = True
        self.vertices -= point
        self.__rotate(x_axis, y_axis, z_axis)
        self.vertices += point
        self.ambiguous = False

    def draw(self, surface, camera):
        """
        Draw the object
        :param surface: the pygame surface to draw on
        :param camera: the camera to draw from
        :return:
        """
        self._wait_for_ambiguous()
        self.drawing = True

        face_distances = get_face_distances(self.faces, self.vertices, camera.position)

        sorted_indices = np.argsort(face_distances)[
            ::-1
        ]  # Sorting indices in descending order

        self.faces = [self.faces[i] for i in sorted_indices]

        moved_vertices = self.vertices - camera.position
        reshaped_vertices = moved_vertices.reshape(-1, 1, moved_vertices.shape[1])
        rotated_vertices = np.sum(camera.rotation_matrix * reshaped_vertices, axis=-1)

        projected_vertices = [
            project_point(
                vertex,
                camera.offset_array,
                camera.focal_length,
            )[0]
            for vertex in rotated_vertices
        ]

        for face in self.faces:
            face_verts = face[0]
            face_color = face[1] if len(face) > 1 else self.color
            face_normal = face[2] if len(face) > 2 else None

            # rotate face normal by object rotation
            if face_normal is not None and self.shadow:
                face_normal = np.dot(face_normal, self.negative_rotation_matrix)

                shadow_normal = ((face_normal[2] + 255) / 510) * 255

                shadow_normal /= self.shadow_effect

                # dim the color based on the shadow_normal
                face_color = tuple(
                    int(color * shadow_normal / 255) for color in face_color
                )

            if any(
                vertex is None
                for vertex in [projected_vertices[vertex] for vertex in face_verts]
            ):
                continue
            pygame.draw.polygon(
                surface,
                face_color,
                [projected_vertices[vertex] for vertex in face_verts],
            )

        self.drawing = False