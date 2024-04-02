from ..object_classes.base_object import Object
import numpy as np
import pygame
from ..point_math.project_point import project_point

pygame.init()


class TextObject(Object):
    def __init__(self, text, position, color=(0, 0, 0), size=1):
        super().__init__(position=position, color=color)
        self.text = text
        self.size = size
        self.show()

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def draw(self, surface, camera):
        # draw text with left corner at position, should also be scaled based on distance from camera
        camera_distance = np.linalg.norm(self.position - camera.position)

        moved_vertices = self.position.copy() - camera.position
        rotated_vertices = np.sum(camera.rotation_matrix * moved_vertices, axis=-1)

        flat_position = project_point(
            rotated_vertices,
            camera.offset_array,
            camera.focal_length,
        )[0]

        if flat_position is not None:

            # scale text based on distance from camera
            scale = 1 / camera_distance

            font = pygame.font.Font("freesansbold.ttf", int(100 * scale * self.size))
            text = font.render(self.text, True, self.color)

            # clamp flat position to be between -10000 and 10000
            flat_position = np.clip(flat_position, -10000, 10000)

            surface.blit(text, flat_position)
