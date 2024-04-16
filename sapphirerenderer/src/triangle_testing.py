from sapphirerenderer import SapphireRenderer
import numpy as np
from time import sleep


def main():
    renderer = SapphireRenderer(draw_axis=True)

    cubes = []

    # 2400 vertices
    for i in range(300):
        cubes.append(
            renderer.add_object(
                "Fcube",
                [
                    np.random.rand(3) * 20,
                    (0, 0, 0),
                    True,
                ],
            )
        )

    while renderer.running:
        for cube in cubes:
            cube.rotate_around_point(0.0, 0.1, 0.1, np.array([0, 0, 0]))
        sleep(0.1)


if __name__ == "__main__":
    main()
