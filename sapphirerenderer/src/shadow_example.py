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

    stl.move_absolute(np.array([2, 0, 0]))

    stl1 = renderer.add_object(
        "Fstl",
        [
            "O:\Python Files\Packages\Sapphire-Renderer\src\sapphirerenderer\objects\suzanne.stl",
            np.array([0, 0, 0]),
            (255, 0, 0),
            False,
            False,
        ],
    )

    stl1.move_absolute(np.array([-2, 0, 0]))

    while renderer.running:
        # stl.rotate_local(0, 1, 0)
        sleep(1)
        continue


if __name__ == "__main__":
    main()
