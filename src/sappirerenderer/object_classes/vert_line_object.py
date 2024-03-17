from object_classes.base_object import Object
import numpy as np
import pygame
from settings import draw_vertices, draw_lines, line_thickness, point_thickness
from point_math.project_point import project_point
from point_math.matricies import get_pitch_yaw_roll_matrix


class VertLineObject(Object):
    def __init__(self, vertices, lines, position=np.array([0, 0, 0], dtype=float), color=(0, 0, 0)):
        super().__init__(position, color)
        self.vertices = vertices
        self.lines = lines
        self.position = np.array([0, 0, 0], dtype=float)
        self.color = color

        self.move(position)

    def move(self, vector):
        self.position += vector
        for i in range(len(self.vertices)):
            self.vertices[i] += vector

    def rotate(self, pitch, yaw, roll):
        rotation_matrix = get_pitch_yaw_roll_matrix(pitch, yaw, roll)
        self.vertices = np.dot(self.vertices, rotation_matrix.T)

    def __str__(self):
        return self.__class__.__name__

    def draw(self, surface, camera):
        if self.lines is not None:
            for line in self.lines:
                start = self.vertices[line[0]]
                end = self.vertices[line[1]]

                start, s_scale = project_point(start, camera.rotation_matrix, camera.position, camera.size, camera.focal_length)
                end, e_scale = project_point(end, camera.rotation_matrix, camera.position, camera.size, camera.focal_length)

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
                vertex, scale = project_point(vertex, camera.rotation_matrix, camera.position, camera.size, camera.focal_length)

                if draw_vertices and vertex is not None:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        vertex,
                        max(int(point_thickness * scale), 1),
                    )
