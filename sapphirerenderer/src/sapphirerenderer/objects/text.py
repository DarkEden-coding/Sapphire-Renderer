from ..object_classes.text_object import TextObject
import numpy as np


class Text(TextObject):
    def __init__(self, text, position=np.array([0, 0, 0]), color=(0, 0, 0), size=1):
        super().__init__(text, position, color, size)
