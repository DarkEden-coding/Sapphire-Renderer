from object_classes.base_object import Object
import numpy as np
import pygame
from settings import draw_vertices, draw_lines, line_thickness, point_thickness
from point_math.project_point import project_point


class VertLineObject(Object):
    def __init__(self, vertices, lines, position=np.array([0, 0, 0]), color=(0, 0, 0)):
        super().__init__(position, color)
        self.vertices = vertices
        self.lines = lines

    def move(self, vector):
        self.position += vector
        self.__move_points()

    def __move_points(self):
        for i in range(len(self.vertices)):
            self.vertices[i] += self.position

    def draw(self, surface, camera):
        for line in self.lines:
            start = self.vertices[line[0]]
            end = self.vertices[line[1]]

            start = project_point(start, camera)
            end = project_point(end, camera)

            if draw_vertices:
                if start is not None:
                    pygame.draw.circle(surface, self.color, start, point_thickness)
                if end is not None:
                    pygame.draw.circle(surface, self.color, end, point_thickness)

            if start is None or end is None:
                continue

            if draw_lines:
                pygame.draw.line(surface, self.color, start, end, line_thickness)
