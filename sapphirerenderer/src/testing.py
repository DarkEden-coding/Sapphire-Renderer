from sapphirerenderer import SapphireRenderer
import numpy as np
from time import sleep


def main():
    renderer = SapphireRenderer(draw_axis=True)

    stl = renderer.add_object(
        "Fstl",
        [
            "O:\Python Files\Packages\Sapphire-Renderer\src\sapphirerenderer\objects\suzanne.stl",
            np.array([0, 0, 0]),
            (255, 0, 0),
            False,
        ],
    )

    grass = renderer.add_object(
        "Grass", args=[np.array([0, 0, 0]), (255, 0, 0), 5, 10, 10, 0.1, 0]
    )

    grass.move_absolute(np.array([-2.5, -2.5, 0]))

    stl.move_absolute(np.array([0, 0, 1]))

    while renderer.running:
        # stl.rotate_local(0, 0.01, 0)
        sleep(0.01)


if __name__ == "__main__":
    main()
