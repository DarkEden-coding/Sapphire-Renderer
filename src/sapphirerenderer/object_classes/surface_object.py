from ..object_classes.base_object import Object
import numpy as np
import pygame
from ..point_math.project_point import project_point
from ..point_math.average_points import average_points

pygame.init()


class SurfaceObject(Object):
    def __init__(self, vertices, color=(0, 0, 0)):
        """
        Object with a single surface
        :param vertices: the vertices of the surface
        :param color: the color of the surface
        """
        self.position = average_points(vertices)
        super().__init__(color=color, position=self.position)
        self.vertices = vertices

        self.drawing = False
        self.ambiguous = False

        self.show()

    def change_vertices(self, vertices):
        """
        Change the vertices of the surface
        :param vertices: the new vertices
        :return:
        """
        self._wait_for_draw()

        self.ambiguous = True
        self.vertices = vertices
        self.position = average_points(vertices)
        self.ambiguous = False

    def draw(self, surface, camera):
        """
        Draw the surface
        :param surface: the pygame surface to draw on
        :param camera: the camera to draw from
        :return:
        """
        self._wait_for_ambiguous()

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

        for vertex in projected_vertices:
            if vertex is None:
                return

        pygame.draw.polygon(surface, self.color, projected_vertices)
