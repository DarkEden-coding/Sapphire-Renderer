from sapphirerenderer import FlatFacesObject
import numpy as np
from scipy import interpolate
from noise import pnoise2  # Assuming you have the 'noise' library installed


class Grass(FlatFacesObject):
    def __init__(
        self,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        size=1,
        rows=5,
        cols=5,
        z_scale=0.1,
        color_randomness=0.1,
        shadow_effect=1,
    ):
        # Generate vertices for a flat grid
        x_vals = np.linspace(0, size, cols)
        y_vals = np.linspace(0, size, rows)
        vertices = np.array([(x, y, 0) for x in x_vals for y in y_vals], dtype=float)
        self.z_scale = z_scale

        # Generate Perlin noise for Z height of vertices
        self.scale_factor = 0.1  # Adjust as needed
        noise_grid = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                noise_grid[i][j] = pnoise2(i * self.scale_factor, j * self.scale_factor)

        # Interpolate the noise to get smooth transitions
        self.interp_func = interpolate.interp2d(
            np.arange(cols), np.arange(rows), noise_grid, kind="linear"
        )

        # Apply Perlin noise to vertices
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                vertices[idx][2] += self.interp_func(j, i) * z_scale

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
