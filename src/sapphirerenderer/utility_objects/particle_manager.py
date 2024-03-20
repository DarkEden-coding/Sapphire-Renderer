import numpy as np
from ..main import SapphireRenderer


class ParticleManager:
    def __init__(self, parent_object, renderer: SapphireRenderer, hide_parent=True):
        self.particles = []
        self.parent_object = parent_object
        self.renderer = renderer

        if hide_parent:
            parent_object.hide()

    def add_particle(self, position=None, color=None):
        """
        Add a particle to the particle manager
        :param position: the position of the particle
        :param color: the color of the particle
        :return: the particle object
        """
        if not hasattr(self.parent_object, "copy"):
            raise AttributeError(
                "The parent object must have a copy method to be used as a particle"
            )

        if position is None:
            position = self.parent_object.get_position()

        if color is None:
            color = self.parent_object.get_color()

        particle = self.renderer.direct_add_object(self.parent_object.copy())
        particle.move_absolute(position)
        particle.set_color(color)

        self.particles.append(particle)

        return particle

    def remove_particle(self, particle):
        """
        Remove a particle from the particle manager
        :param particle: the particle to remove
        """
        self.particles.remove(particle)
        self.renderer.remove_object(particle)

    def clear_particles(self):
        """
        Remove all particles from the particle manager
        """
        for particle in self.particles:
            self.renderer.remove_object(particle)
        self.particles = []

    def move_particles(self, movement):
        """
        Move all particles by a certain amount
        :param movement: the amount to move the particles by
        """
        for particle in self.particles:
            particle.move_relative(movement)
