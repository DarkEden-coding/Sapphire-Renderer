from ..object_classes.base_object import Object
import numpy as np
import pygame
from ..point_math.project_point import project_point

pygame.init()


class TextObject(Object):
    def __init__(self, text, position, color=(0, 0, 0), size=1):
        """
        Object to display text
        :param text: the text to display
        :param position: the position of the text
        :param color: the color of the text
        :param size: the size of the text
        """
        super().__init__(position=position, color=color)
        self.text = text
        self.size = size
        self.compile_verts = False
        self.show()

    def set_text(self, text):
        """
        Set the text
        :param text: the new text
        :return:
        """
        self.text = text

    def get_text(self):
        """
        Get the text
        :return: the text
        """
        return self.text

    def draw(self, renderer):
        """
        Draw the text
        :param renderer: the renderer to draw with
        :return:
        """
        camera = renderer.camera
        surface = renderer.display
        display_size = renderer.display_size

        # draw text with left corner at position, should also be scaled based on distance from camera
        camera_distance = np.linalg.norm(self.position - camera.position)

        moved_vertices = self.position.copy() - camera.position
        rotated_vertices = np.sum(camera.rotation_matrix * moved_vertices, axis=-1)

        flat_position = project_point(
            rotated_vertices,
            camera.offset_array,
            camera.focal_length,
            display_size,
            camera.fov_side,
            camera.fov_top,
        )[0]

        if flat_position is not None:

            # scale text based on distance from camera
            scale = 1 / camera_distance

            font = pygame.font.Font("freesansbold.ttf", int(100 * scale * self.size))
            text = font.render(self.text, True, self.color)

            # clamp flat position to be between -10000 and 10000
            flat_position = np.clip(flat_position, -10000, 10000)

            surface.blit(text, flat_position)
