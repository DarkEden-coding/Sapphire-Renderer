import numpy as np
from stl import mesh
from ..object_classes.flat_faces_object import FlatFacesObject


class Fstl(FlatFacesObject):
    def __init__(
        self,
        filename,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        random_color=False,
        shadow=True,
    ):
        # Load STL file
        mesh_data = mesh.Mesh.from_file(filename)

        # Extract vertices
        vertices = np.unique(mesh_data.vectors.reshape(-1, 3), axis=0)

        # Extract faces
        faces = []
        for triangle in mesh_data.vectors:
            face_vertices = []
            for vertex in triangle:
                index = np.nonzero((vertices == vertex).all(axis=1))[0][0]
                face_vertices.append(index)
            (
                faces.append([face_vertices, color])
                if not random_color
                else faces.append([face_vertices, np.random.randint(0, 255, 3)])
            )

        normals = mesh_data.normals
        for i, face in enumerate(faces):
            face.append(normals[i] / np.linalg.norm(normals[i]) * 255)

        faces = [tuple(face) for face in faces]

        super().__init__(vertices, faces, position, color, shadow)
