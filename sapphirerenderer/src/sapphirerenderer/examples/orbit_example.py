from sapphirerenderer import SapphireRenderer
import numpy as np
from time import sleep


def main():
    renderer = SapphireRenderer(draw_axis=True)

    large_cube = renderer.add_object(
        "Cube", args=(np.array([0, 0, 0], dtype=float), (0, 255, 0), 1)
    )
    small_cube = renderer.add_object(
        "Cube", args=(np.array([4, 0, 0], dtype=float), (255, 0, 0), 0.5)
    )

    large_text = renderer.add_object(
        "Text", args=("Large Cube", np.array([0, 0, 0]), (0, 0, 0))
    )

    small_text = renderer.add_object(
        "Text", args=("Small Cube", np.array([4, 0, 0]), (0, 0, 0), 0.5)
    )

    large_vector = np.array([0, 0, 0], dtype=float)
    small_vector = np.array([0, 0.05, 0.05], dtype=float)

    large_mass = 1
    small_mass = 0.5
    gravitational_constant = 9.81

    while renderer.running:
        gravitational_force = (
            gravitational_constant
            * large_mass
            * small_mass
            / np.linalg.norm(large_cube.center_point - small_cube.center_point) ** 2
        )

        large_acceleration = gravitational_force / large_mass
        small_acceleration = gravitational_force / small_mass

        # make vector that points from large cube to small cube with a magnitude of large acceleration
        large_accel_vector = (
            (small_cube.center_point - large_cube.center_point)
            * large_acceleration
            / 1000
        )
        small_accel_vector = (
            (large_cube.center_point - small_cube.center_point)
            * small_acceleration
            / 1000
        )

        large_vector += large_accel_vector
        small_vector += small_accel_vector

        # large_cube.move_relative(large_vector)
        small_cube.move_relative(small_vector)

        small_text.set_position(small_cube.center_point)

        sleep(0.01)


if __name__ == "__main__":
    main()
