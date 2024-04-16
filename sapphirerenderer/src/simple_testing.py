from sapphirerenderer import SapphireRenderer
import numpy as np
from time import sleep


def main():
    renderer = SapphireRenderer(draw_axis=True)

    cubes = []

    # 4800 vertices
    for i in range(600):
        cubes.append(
            renderer.add_object(
                "Cube",
                [
                    np.random.rand(3) * 20,
                    (0, 0, 0),
                    True,
                ],
            )
        )

    for cube in cubes:
        cube.rotate_around_point(45.0, 0.0, 0.0, np.array([0, 0, 0]))
        continue

    while renderer.running:
        for cube in cubes:
            cube.rotate_local(0, 1, 0)
        sleep(0.01)


if __name__ == "__main__":
    main()
