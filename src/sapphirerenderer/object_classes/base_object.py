import numpy as np
from time import sleep


class Object:
    def __init__(
        self,
        position=np.array([0, 0, 0]),
        rotation=np.array((0, 0, 0)),
        scale=1,
        color=(0, 0, 0),
    ):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.hidden = True
        self.color = color

        self.drawing = False
        self.ambiguous = False

    def _wait_for_draw(self):
        while self.drawing:
            sleep(0.001)

    def _wait_for_ambiguous(self):
        while self.ambiguous:
            sleep(0.001)

    def is_hidden(self):
        return self.hidden

    def hide(self):
        self.hidden = True
        return self

    def show(self):
        self.hidden = False
        return self

    def set_position(self, position):
        self.position = position

    def move_relative(self, vector):
        self.position += vector

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_scale(self, scale):
        self.scale = scale

    def set_color(self, color):
        self.color = color

    def get_position(self):
        return self.position

    def get_rotation(self):
        return self.rotation

    def get_scale(self):
        return self.scale

    def get_color(self):
        return self.color

    def update(self):
        """
        empty update for child classes to override
        :return:
        """
        pass

    def __str__(self):
        return self.__class__.__name__
