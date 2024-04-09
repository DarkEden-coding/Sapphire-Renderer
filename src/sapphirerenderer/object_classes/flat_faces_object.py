from ..object_classes.base_object import Object
import pygame
from ..point_math.average_points import average_points
import numpy as np
from ..point_math.project_point import project_point
from ..point_math.matricies import get_pitch_yaw_roll_matrix

pygame.init()


class FlatFacesObject(Object):
    def __init__(self, vertices, faces, position=np.array([0, 0, 0]), color=(0, 0, 0)):
        self.original_vertices = vertices.copy()
        self.center_point = average_points(vertices)
        self.position = position

        super().__init__(color=color, position=self.position)
        self.vertices = vertices
        self.faces = faces
        self.rotation = np.array([0, 0, 0], dtype=float)

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
        self.ambiguous = False

    def rotate_local(self, x_axis, y_axis, z_axis):
        self._wait_for_draw()

        self.ambiguous = True
        self.vertices -= self.center_point
        self.__rotate(x_axis, y_axis, z_axis)
        self.vertices += self.center_point
        self.ambiguous = False

    def rotate_around_point(
        self, x_axis, y_axis, z_axis, point=np.array([0, 0, 0], dtype=float)
    ):
        self._wait_for_draw()

        self.ambiguous = True
        self.vertices -= point
        self.__rotate(x_axis, y_axis, z_axis)
        self.vertices += point
        self.ambiguous = False

    def draw(self, surface, camera):
        self._wait_for_ambiguous()
        self.drawing = True

        # sort faces by inverse distance from camera
        face_distances = [
            np.linalg.norm(vertex - camera.position) for vertex in self.vertices
        ]

        # Sort faces by the mean of inverse distances from camera
        self.faces = sorted(
            self.faces,
            key=lambda face: np.mean([face_distances[vertex] for vertex in face[0]]),
            reverse=True,
        )

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
