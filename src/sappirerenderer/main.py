import threading
import os
from utility_objects.camera import Camera
import numpy as np
from settings import camera_move_speed, camera_rotate_speed, fps, show_fps
from time import time


class SapphireRenderer:
    def __init__(self, width=500, height=500):
        """
        Initialize the renderer
        :param width: Width of the window
        :param height: Height of the window
        """
        self.display = None

        self.width = width
        self.height = height

        self.camera = Camera(self, position=np.array((0.0, -3.0, 0.0)))

        self.objects = []
        self.load_objects()

        self.running = True

        self.thread = threading.Thread(target=self.render_loop)
        self.thread.start()

    def load_objects(self):
        # go through all files in objects and load them
        for file in os.listdir("objects"):
            if file.endswith(".py"):
                exec(f"from objects.{file[:-3]} import *")
                self.add_object(eval(f"{file[:1].upper()}{file[1:-3]}()"))

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        self.camera.update()
        for obj in self.objects:
            obj.update()

    def user_input(self, pygame):
        # wasd to move camera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.move_relative((camera_move_speed, 0, 0))
        if keys[pygame.K_s]:
            self.camera.move_relative((-camera_move_speed, 0, 0))
        if keys[pygame.K_a]:
            self.camera.move_relative((0, camera_move_speed, 0))
        if keys[pygame.K_d]:
            self.camera.move_relative((0, -camera_move_speed, 0))
        if keys[pygame.K_q]:
            self.camera.move_relative((0, 0, camera_move_speed))
        if keys[pygame.K_e]:
            self.camera.move_relative((0, 0, -camera_move_speed))

        if keys[pygame.K_LEFT]:
            self.camera.rotate_relative((0, -camera_rotate_speed))
        if keys[pygame.K_RIGHT]:
            self.camera.rotate_relative((0, camera_rotate_speed))
        if keys[pygame.K_UP]:
            self.camera.rotate_relative((camera_rotate_speed, 0))
        if keys[pygame.K_DOWN]:
            self.camera.rotate_relative((-camera_rotate_speed, 0))

    def render_loop(self):
        import pygame

        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill((255, 255, 255))
        pygame.display.set_caption("Sapphire Renderer")

        while self.running:
            frame_start = time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.user_input(pygame)

            self.display.fill((255, 255, 255))
            self.update()

            for obj in self.objects:
                obj.draw(self.display, self.camera)
            pygame.display.flip()

            pygame.time.Clock().tick(fps)

            if show_fps:
                pygame.display.set_caption(
                    f"Sapphire Renderer - FPS: {int(1 / (time() - frame_start))}"
                )

        pygame.quit()

    def stop(self):
        self.running = False
        self.thread.join()


renderer = SapphireRenderer()
