import numpy as np
from stl import mesh
from src.sapphirerenderer.object_classes.vert_line_object import VertLineObject


class Stl(VertLineObject):
    def __init__(self, filename, position=np.array([0.0, 0.0, 0.0]), color=(0, 0, 0)):
        # Load STL file
        mesh_data = mesh.Mesh.from_file(filename)

        # Extract vertices
        vertices = np.unique(mesh_data.vectors.reshape(-1, 3), axis=0)

        # Generate line segments
        line_segments = []
        for triangle in mesh_data.vectors:
            for i in range(3):
                p1 = np.nonzero((vertices == triangle[i]).all(axis=1))[0][0]
                p2 = np.nonzero((vertices == triangle[(i + 1) % 3]).all(axis=1))[0][0]
                line_segments.append((p1, p2))

        super().__init__(vertices, np.array(line_segments), position, color)

    def update(self):
        self.rotate(0.01, 0.01, 0.01)
