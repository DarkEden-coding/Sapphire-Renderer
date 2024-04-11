import numpy as np
from ..object_classes.flat_faces_object import FlatFacesObject


def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("v "):
                vertex = [float(coord) for coord in line.split()[1:]]
                vertices.append(vertex)
            elif line.startswith("f "):
                face_data = [
                    [int(index.split("/")[0]) - 1 for index in line.split()[1:]]
                ]
                faces.append(face_data)

    return np.array(vertices), faces


class Fobj(FlatFacesObject):
    def __init__(
        self,
        filename,
        position=np.array([0.0, 0.0, 0.0]),
        color=(0, 0, 0),
        random_color=False,
    ):
        if not filename.endswith(".obj"):
            raise ValueError("File must be an OBJ file")

        # Load OBJ file
        vertices, faces = load_obj(filename)

        for face in faces:
            if not random_color:
                face.append(color)
            else:
                face.append(np.random.randint(0, 255, 3))

        super().__init__(vertices, faces, position, color, True)
