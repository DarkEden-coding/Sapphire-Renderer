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


class VertLineObject(Object):
    def __init__(
        self,
        vertices,
        lines,
        position=np.array([0, 0, 0], dtype=float),
        color=(0, 0, 0),
    ):
        super().__init__(position, color)
        self.original_vertices = vertices
        self.vertices = vertices
        self.lines = lines
        self.position = np.array([0, 0, 0], dtype=float)
        self.color = color

        self.move_absolute(position)

    def move_relative(self, vector):
        """
        Move the object by a relative amount
        :param vector: the amount to move by
        :return:
        """
        self.position += vector
        for i in range(len(self.vertices)):
            self.vertices[i] += vector

    def move_absolute(self, vector):
        """
        Move the object to an absolute position
        :param vector: the position to move to
        :return:
        """
        self.position = vector
        for i in range(len(self.vertices)):
            self.vertices[i] = self.original_vertices[i] + vector

    def rotate(self, pitch, yaw, roll):
        rotation_matrix = get_pitch_yaw_roll_matrix(pitch, yaw, roll)
        self.vertices = np.dot(self.vertices, rotation_matrix.T)

    def __str__(self):
        return self.__class__.__name__

    def draw(self, surface, camera):
        moved_vertices = self.vertices - camera.position
        reshaped_vertices = moved_vertices.reshape(-1, 1, moved_vertices.shape[1])
        rotated_vertices = np.sum(camera.rotation_matrix * reshaped_vertices, axis=-1)

        if self.lines is not None:
            for line in self.lines:
                start = rotated_vertices[line[0]]
                end = rotated_vertices[line[1]]

                start, s_scale = project_point(
                    start,
                    camera.offset_array,
                    camera.focal_length,
                )
                end, e_scale = project_point(
                    end,
                    camera.offset_array,
                    camera.focal_length,
                )

                if draw_vertices:
                    if start is not None:
                        pygame.draw.circle(
                            surface,
                            self.color,
                            start,
                            max(int(point_thickness * s_scale), 1),
                        )
                    if end is not None:
                        pygame.draw.circle(
                            surface,
                            self.color,
                            end,
                            max(int(point_thickness * e_scale), 1),
                        )

                if start is None or end is None:
                    continue

                if draw_lines:
                    pygame.draw.line(
                        surface,
                        line[2] if len(line) > 2 else self.color,
                        start,
                        end,
                        max(int(line_thickness * (s_scale + e_scale) / 2), 1),
                    )
        else:
            for vertex in self.vertices:
                vertex, scale = project_point(
                    vertex,
                    camera.offset_array,
                    camera.focal_length,
                )

                if draw_vertices and vertex is not None:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        vertex,
                        max(int(point_thickness * scale), 1),
                    )
