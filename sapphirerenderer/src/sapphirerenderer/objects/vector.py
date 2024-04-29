from ..object_classes.flat_faces_object import FlatFacesObject
import numpy as np


class Vector(FlatFacesObject):
    def __init__(
        self,
        start_point=np.array([0.0, 0.0, 0.0]),
        rotation=np.array([0.0, 0.0, 0.0]),
        length=1,
        color=(0, 0, 0),
        thickness=0.02,
    ):
        """
        Vector object
        :param start_point: the start point of the vector
        :param rotation: the rotation of the vector
        :param length: the length of the vector
        :param color: the color of the vector
        :param thickness: the thickness of the vector
        """

        vertices = []
        faces = []
        pi2 = np.pi * 2

        for i in range(max(round(length * 4), 1)):
            vertices.append(
                np.array(
                    [np.cos(pi2 / 3) * thickness, np.sin(pi2 / 3) * thickness, i / 4]
                )
            )
            vertices.append(
                np.array(
                    [
                        np.cos(pi2 * 2 / 3) * thickness,
                        np.sin(pi2 * 2 / 3) * thickness,
                        i / 4,
                    ]
                )
            )
            vertices.append(
                np.array([np.cos(pi2) * thickness, np.sin(pi2) * thickness, i / 4])
            )

        vertices.append(
            np.array(
                [
                    np.cos(pi2 / 3) * thickness,
                    np.sin(pi2 / 3) * thickness,
                    length - 0.03,
                ]
            )
        )
        vertices.append(
            np.array(
                [
                    np.cos(pi2 * 2 / 3) * thickness,
                    np.sin(pi2 * 2 / 3) * thickness,
                    length - 0.03,
                ]
            )
        )
        vertices.append(
            np.array([np.cos(pi2) * thickness, np.sin(pi2) * thickness, length - 0.03])
        )

        # make faces between the vertices so that outside of the vector is filled in
        # ex: (0, 1, 3, 4) makes a face between the two ends of the vector
        for i in range(0, len(vertices) - 3, 3):
            for j in range(3):
                if j == 2:
                    faces.append(
                        (
                            [i + 2, i, i + 3, i + 5],
                            color,
                        )
                    )
                else:
                    faces.append(
                        (
                            [i + j, i + j + 1, i + j + 4, i + j + 3],
                            color,
                        )
                    )

        # make arrow head
        for i in range(4):
            vertices.append(
                np.array(
                    [
                        np.cos(pi2 * (i + 1) / 4) * thickness * 2,
                        np.sin(pi2 * (i + 1) / 4) * thickness * 2,
                        length - 0.03,
                    ],
                )
            )
        vertices.append(np.array([0, 0, length], dtype=float))

        faces.append(([len(vertices) - 5, len(vertices) - 4, len(vertices) - 1], color))
        faces.append(
            (
                [len(vertices) - 4, len(vertices) - 3, len(vertices) - 1],
                color,
            )
        )
        faces.append(
            (
                [len(vertices) - 3, len(vertices) - 2, len(vertices) - 1],
                color,
            )
        )
        faces.append(
            (
                [len(vertices) - 2, len(vertices) - 5, len(vertices) - 1],
                color,
            )
        )

        super().__init__(
            vertices=vertices,
            faces=faces,
            color=color,
            compile_verts=True,
            position=start_point,
        )
