from ..object_classes.base_object import Object
import numpy as np
import pygame
from ..settings import (
    draw_vertices,
    draw_lines,
    line_thickness,
    point_thickness,
)
from ..point_math.project_point import project_point
from ..point_math.matricies import get_pitch_yaw_roll_matrix
from ..point_math.average_points import average_points
from time import sleep


class VertLineObject(Object):
    def __init__(
        self,
        vertices,
        lines,
        position=np.array([0, 0, 0], dtype=float),
        color=(0, 0, 0),
    ):
        super().__init__(position=position, color=color)
        self.original_vertices = vertices.copy()
        self.vertices = vertices
        self.lines = lines
        self.position = np.array([0, 0, 0], dtype=float)
        self.color = color
        self.rotation = np.array([0, 0, 0], dtype=float)

        self.center_point = average_points(self.vertices)

        self.drawing = False
        self.ambiguous = False

        self.move_absolute(position)

        self.show()

    def _wait_for_draw(self):
        while self.drawing:
            sleep(0.001)

    def _wait_for_ambiguous(self):
        while self.ambiguous:
            sleep(0.001)

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

    def __str__(self):
        return self.__class__.__name__

    def draw(self, surface, camera):
        self._wait_for_ambiguous()

        moved_vertices = self.vertices - camera.position
        reshaped_vertices = moved_vertices.reshape(-1, 1, moved_vertices.shape[1])
        rotated_vertices = np.sum(camera.rotation_matrix * reshaped_vertices, axis=-1)

        projected_vertices = [
            project_point(
                vertex,
                camera.offset_array,
                camera.focal_length,
            )
            for vertex in rotated_vertices
        ]

        if self.lines is not None and draw_lines:
            for line in self.lines:
                start, s_scale = projected_vertices[line[0]]
                end, e_scale = projected_vertices[line[1]]

                if start is None or end is None:
                    continue

                pygame.draw.line(
                    surface,
                    line[2] if len(line) > 2 else self.color,
                    start,
                    end,
                    max(int(line_thickness * (s_scale + e_scale) / 2), 1),
                )
        if draw_vertices:
            for vertex in projected_vertices:
                vertex, scale = vertex

                if draw_vertices and vertex is not None:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        vertex,
                        max(int(point_thickness * scale), 1),
                    )
