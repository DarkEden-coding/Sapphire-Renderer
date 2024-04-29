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
from .point_math.project_point import project_point
from .object_classes.flat_faces_object import get_face_distances
import pygame

average_fps_list = []


class SapphireRenderer:
    def __init__(
        self, width=1000, height=1000, draw_axis=False, movement_handling=True
    ):
        """
        Initialize the renderer
        :param width: Width of the window
        :param height: Height of the window
        :param draw_axis: Draws the axis lines, use-full for debugging
        ;param: movement_handling: Whether to handle movement of the camera
        """
        self.display = None

        self.movement_handling = movement_handling

        self.width = width
        self.height = height
        self.display_size = (width, height)

        self.camera_rotate_speed = camera_rotate_speed
        self.camera_move_speed = camera_move_speed

        self.camera = Camera(self, position=np.array((0.0, -3.0, 0.0)))

        self.loaded_objects = []
        self.instance_objects = []
        self.load_objects()

        if draw_axis:
            self.add_object("Axes")

        self.running = True

        self.thread = threading.Thread(target=self.render_loop)
        self.thread.start()

    @staticmethod
    def get_pygame_object():
        return pygame

    def load_objects(self):
        # go through all files in objects and load them
        for file in os.listdir(os.path.dirname(__file__) + "/objects"):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    exec(f"from .objects.{file[:-3]} import *")
                    obj_class_name = f"{file[:1].upper().replace('_', '')}{file[1:-3].replace('_', '')}"
                    self.loaded_objects.append((obj_class_name, eval(obj_class_name)))
                except Exception as e:
                    print(f"Failed to load object {file}: {e}")

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
            self.camera.move_relative((self.camera_move_speed * scale_factor, 0, 0))
        if keys[pygame.K_s]:
            self.camera.move_relative((-self.camera_move_speed * scale_factor, 0, 0))
        if keys[pygame.K_a]:
            self.camera.move_relative((0, self.camera_move_speed * scale_factor, 0))
        if keys[pygame.K_d]:
            self.camera.move_relative((0, -self.camera_move_speed * scale_factor, 0))
        if keys[pygame.K_q]:
            self.camera.move_relative((0, 0, -self.camera_move_speed * scale_factor))
        if keys[pygame.K_e]:
            self.camera.move_relative((0, 0, self.camera_move_speed * scale_factor))

        if keys[pygame.K_LEFT]:
            self.camera.rotate_relative((0, -self.camera_rotate_speed * scale_factor))
        if keys[pygame.K_RIGHT]:
            self.camera.rotate_relative((0, self.camera_rotate_speed * scale_factor))
        if keys[pygame.K_UP]:
            self.camera.rotate_relative((-self.camera_rotate_speed * scale_factor, 0))
        if keys[pygame.K_DOWN]:
            self.camera.rotate_relative((self.camera_rotate_speed * scale_factor, 0))

    def compiled_draw(self, surface, camera):
        """
        Draw the compiled objects were all verts and faces are put together, sorted, and drawn
        :param surface: the pygame surface to draw on
        :param camera: the camera to draw from
        :return:
        """
        compiled_faces = []
        compiled_verts = []
        index_offset = 0

        # Filter objects that need compilation
        compile_objs = [
            obj
            for obj in self.instance_objects
            if obj.compile_verts and not obj.is_hidden()
        ]
        if not compile_objs:
            return

        for obj in compile_objs:
            obj.drawing = True
            obj.wait_for_ambiguous()

            compiled_verts.extend(obj.vertices.copy())

            # append if the object has shadow, the strength of shadow, and the reverse rotation matrix to each face
            for face in obj.faces:
                if len(face) == 3:
                    face = (
                        [vertex + index_offset for vertex in face[0]],
                        face[1],
                        face[2],
                    )
                else:
                    face = (
                        [vertex + index_offset for vertex in face[0]],
                        face[1],
                        None,
                    )

                compiled_faces.append(
                    face
                    + (
                        obj.shadow,
                        obj.shadow_effect,
                        obj.negative_rotation_matrix,
                    )
                )
            obj.drawing = False
            index_offset += len(obj.vertices)

        face_distances = get_face_distances(
            compiled_faces, compiled_verts, camera.position
        )

        sorted_indices = np.argsort(face_distances)[
            ::-1
        ]  # Sorting indices in descending order

        compiled_faces = [compiled_faces[i] for i in sorted_indices]

        moved_vertices = np.array(compiled_verts) - camera.position
        reshaped_vertices = moved_vertices.reshape(-1, 1, moved_vertices.shape[1])
        rotated_vertices = np.sum(camera.rotation_matrix * reshaped_vertices, axis=-1)

        projected_vertices = [
            project_point(
                vertex,
                camera.offset_array,
                camera.focal_length,
                self.display_size,
                self.camera.fov_side,
                self.camera.fov_top,
            )[0]
            for vertex in rotated_vertices
        ]

        for face in compiled_faces:
            face_verts = face[0]

            valid_verts = [
                vertex
                for vertex in [projected_vertices[vertex] for vertex in face_verts]
                if vertex is not None
            ]
            if len(valid_verts) < 3:
                continue

            face_color = face[1]
            face_normal = face[2]
            face_shadow = face[3]

            if not face_shadow:
                pygame.draw.polygon(
                    surface,
                    face_color,
                    valid_verts,
                )
                continue

            shadow_effect = face[4]
            negative_rotation_matrix = face[5]

            # rotate face normal by object rotation
            if face_normal is not None:
                face_normal = np.dot(face_normal, negative_rotation_matrix)

                shadow_normal = ((face_normal[2] + 255) / 510) * 255

                shadow_normal /= shadow_effect

                # if shadow_normal is nan, set it to 255
                if np.isnan(shadow_normal):
                    shadow_normal = 255

                red = int(face_color[0] * shadow_normal / 255)
                green = int(face_color[1] * shadow_normal / 255)
                blue = int(face_color[2] * shadow_normal / 255)

                # dim the color based on the shadow_normal
                face_color = (red, green, blue)

            pygame.draw.polygon(
                surface,
                face_color,
                valid_verts,
            )

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

            # sort objects by distance from camera, reverse so that objects closer to camera are drawn last
            self.instance_objects.sort(
                key=lambda obj: np.linalg.norm(obj.position - self.camera.position),
                reverse=True,
            )

            self.compiled_draw(self.display, self.camera)

            for obj in self.instance_objects:
                if not obj.is_hidden() and not obj.compile_verts:
                    obj.draw(self)

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

            if self.movement_handling:
                self.user_input(pygame, fps / real_fps)

        pygame.quit()

    def stop(self):
        self.running = False
        self.thread.join()
