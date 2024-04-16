from ..object_classes.flat_faces_object import FlatFacesObject
import numpy as np


class Grass(FlatFacesObject):
    def __init__(
        self,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        size=1,
        rows=5,
        cols=5,
        z_randomness=0.1,
        color_randomness=0.1,
        shadow_effect=1,
    ):
        # Generate vertices for a flat grid
        x_vals = np.linspace(0, size, cols)
        y_vals = np.linspace(0, size, rows)
        vertices = np.array([(x, y, 0) for x in x_vals for y in y_vals], dtype=float)

        # Adding randomness to Z height of vertices
        vertices[:, 2] += np.random.uniform(
            -z_randomness, z_randomness, size=vertices.shape[0]
        )

        # Generate faces for the grid
        faces = []
        for i in range(rows - 1):
            for j in range(cols - 1):
                idx = i * cols + j
                v0_idx = idx
                v1_idx = idx + 1
                v2_idx = idx + cols + 1
                v3_idx = idx + cols
                face_indices = [v0_idx, v1_idx, v2_idx, v3_idx]
                face_color = (0, 255, 0)  # Green color

                # Adding slight variations to green color
                color_array = np.array(face_color, dtype=float)
                color_array += np.random.uniform(
                    -color_randomness * 255, color_randomness * 255, size=3
                )
                color_array = np.clip(color_array, 0, 255).astype(int)

                # Calculate face normal
                v0 = vertices[v0_idx]
                v1 = vertices[v1_idx]
                v2 = vertices[v2_idx]
                normal = np.cross(v1 - v0, v2 - v0)
                normal = normal / np.linalg.norm(normal) * 255

                normal = -normal

                faces.append((face_indices, tuple(color_array), normal))

        super().__init__(vertices, faces, position, color, True, shadow_effect)
