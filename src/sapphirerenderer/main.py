import os
from .utility_objects.camera import Camera
import numpy as np
from .settings import (
    camera_move_speed,
    camera_rotate_speed,
    fps,
    show_fps,
    lock_fps,
)
from time import time
import threading

average_fps_list = []


class SapphireRenderer:
    def __init__(self, width=1000, height=1000, draw_axis=False, object_files=None):
        """
        Initialize the renderer
        :param width: Width of the window
        :param height: Height of the window
        :param draw_axis: Draws the axis lines, use-full for debugging
        ;param: object_files: Used for loading different objects, a list of python file paths
        """
        self.display = None

        self.width = width
        self.height = height

        self.camera = Camera(self, position=np.array((0.0, -3.0, 0.0)))

        self.loaded_objects = []
        self.instance_objects = []
        self.load_objects()

        if draw_axis:
            self.add_object("Axes")

        self.running = True

        self.thread = threading.Thread(target=self.render_loop)
        self.thread.start()

    def load_objects(self):
        # go through all files in objects and load them
        for file in os.listdir(os.path.dirname(__file__) + "/objects"):
            if file.endswith(".py"):
                try:
                    exec(f"from .objects.{file[:-3]} import *")
                    obj_class_name = f"{file[:1].upper().replace('_', '')}{file[1:-3].replace('_', '')}"
                    self.loaded_objects.append((obj_class_name, eval(obj_class_name)))
                except NameError:
                    print(f"Error loading object from file {file}")

    def add_object(self, obj_name, args=None):
        """
        Adds an object to the scene
        :param obj_name: The class name of the object
        :param args: The args to pass to the init of the class
        :return: returns the object created
        """
        for obj_class_name, obj_class in self.loaded_objects:
            if obj_class_name == obj_name:
                obj = obj_class(*args) if args is not None else obj_class()
                self.instance_objects.append(obj)
                return obj

    def direct_add_object(self, obj):
        """
        Adds an object to the scene
        :param obj: The object to add
        :return:
        """
        self.instance_objects.append(obj)
        return obj

    def remove_object(self, obj):
        """
        Removes an object from the scene
        :param obj: The object to remove
        :return:
        """
        self.instance_objects.remove(obj)

    def update(self):
        self.camera.update()
        for obj in self.instance_objects:
            obj.update()

    def user_input(self, pygame, scale_factor=1.0):
        # wasd to move camera
        keys = pygame.key.get_pressed()
        # if shift is pressed, move faster
        if keys[pygame.K_LSHIFT]:
            scale_factor *= 2

        if keys[pygame.K_w]:
            self.camera.move_relative((camera_move_speed * scale_factor, 0, 0))
        if keys[pygame.K_s]:
            self.camera.move_relative((-camera_move_speed * scale_factor, 0, 0))
        if keys[pygame.K_a]:
            self.camera.move_relative((0, camera_move_speed * scale_factor, 0))
        if keys[pygame.K_d]:
            self.camera.move_relative((0, -camera_move_speed * scale_factor, 0))
        if keys[pygame.K_q]:
            self.camera.move_relative((0, 0, -camera_move_speed * scale_factor))
        if keys[pygame.K_e]:
            self.camera.move_relative((0, 0, camera_move_speed * scale_factor))

        if keys[pygame.K_LEFT]:
            self.camera.rotate_relative((0, -camera_rotate_speed * scale_factor))
        if keys[pygame.K_RIGHT]:
            self.camera.rotate_relative((0, camera_rotate_speed * scale_factor))
        if keys[pygame.K_UP]:
            self.camera.rotate_relative((-camera_rotate_speed * scale_factor, 0))
        if keys[pygame.K_DOWN]:
            self.camera.rotate_relative((camera_rotate_speed * scale_factor, 0))

    def render_loop(self):
        import pygame

        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill((255, 255, 255))
        pygame.display.set_caption("Sapphire Renderer")

        while self.running:
            frame_start = time() + 0.00001

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill((255, 255, 255))
            self.update()

            instance_objects = self.instance_objects.copy()

            # sort objects by distance from camera, reverse so that objects closer to camera are drawn last
            instance_objects.sort(
                key=lambda obj: np.linalg.norm(obj.position - self.camera.position),
                reverse=True,
            )

            for obj in instance_objects:
                if not obj.is_hidden():
                    obj.draw(self.display, self.camera)

            pygame.display.flip()

            # if fps is higher than fps setting, wait
            if lock_fps and time() - frame_start < 1 / fps:
                pygame.time.wait(int(1000 * (1 / fps - (time() - frame_start))))

            real_fps = 1 / (time() - frame_start)
            average_fps_list.append(real_fps)

            average_fps = sum(average_fps_list) / len(average_fps_list)

            if len(average_fps_list) > 10:
                average_fps_list.pop(0)

            if show_fps:
                pygame.display.set_caption(
                    f"Sapphire Renderer - FPS: {int(average_fps)}"
                )

            self.user_input(pygame, fps / real_fps)

        pygame.quit()

    def stop(self):
        self.running = False
        self.thread.join()
