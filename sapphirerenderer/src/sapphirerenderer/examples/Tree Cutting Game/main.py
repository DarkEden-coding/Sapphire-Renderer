from sapphirerenderer import SapphireRenderer
from game_objects.grass import Grass
import numpy as np
from time import sleep, time
from threading import Thread
import os


def get_low_point(verts, center):
    lower_bound = min(verts, key=lambda x: x[2])[2]
    return center[0], center[1], lower_bound


def cut_down_tree(tree_index, renderer, trees, tree_colliders, grass):
    tree_colliders[tree_index][1] = False

    tree = trees[tree_index]
    # animate the tree falling over
    for _ in range(900):
        tree.rotate_around_point(
            0.1, 0, 0, get_low_point(tree.vertices, tree.center_point)
        )
        sleep(0.001)
    sleep(2)

    tree_index = trees.index(tree)

    renderer.remove_object(tree_colliders[tree_index][0])
    tree_colliders.pop(tree_index)
    renderer.remove_object(trees[tree_index])
    trees.pop(tree_index)

    # make a new tree that then grows
    sleep(10)

    # make new tree and move the tree so the lowest point of the tree is at the grass vertex
    new_tree = renderer.add_object(
        "Fstl",
        args=[
            "SpruceTree1.stl",
            np.array([0, 0, 0]),
            (0, 255, 0),
            False,
            True,
        ],
    )
    new_tree.set_scale(0.00001)
    new_tree.rotate_local(90, 0, 0)

    verts = new_tree.vertices
    center = new_tree.center_point

    grass_vertex = grass.vertices[np.random.randint(0, len(grass.vertices))]

    new_tree.move_absolute(
        np.array(grass_vertex) - np.array(get_low_point(verts, center))
    )

    # make a collider for the tree
    collider = renderer.add_object(
        "Cuboid",
        args=[
            np.array([0, 0, 0]),
            np.array([0.25, 0.25, 1]),
            np.array(grass_vertex),
            (255, 0, 0),
        ],
    )

    collider.hide()

    # move collider to the lowest point of the tree
    collider.move_absolute(np.array(grass_vertex) - np.array([0.125, 0.125, 0]))

    trees.append(new_tree)
    tree_colliders.append([collider, False])

    grow_tree(new_tree, tree_colliders, collider)


def grow_tree(tree, tree_colliders, collider):
    for _ in range(4500):
        tree.set_scale(
            tree.scale + 0.001, get_low_point(tree.vertices, tree.center_point)
        )
        sleep(0.0001)

    collider_index = tree_colliders.index([collider, False])
    tree_colliders[collider_index][1] = True


def main():
    renderer = SapphireRenderer()
    renderer.camera_move_speed = 0.01
    money = 0

    grass = Grass(
        color=(0, 255, 0), size=10, rows=40, cols=40, color_randomness=0.1, z_scale=0.3
    )

    grass = renderer.direct_add_object(grass)

    trees = []
    tree_colliders = []

    # get current path
    current_path = os.path.dirname(os.path.abspath(__file__))
    tree_path = os.path.join(current_path, "SpruceTree1.stl")

    # make 5 trees put at random grass vertices
    for _ in range(20):
        # make new tree and move the tree so the lowest point of the tree is at the grass vertex
        new_tree = renderer.add_object(
            "Fstl",
            args=[
                tree_path,
                np.array([0, 0, 0]),
                (0, 255, 0),
                False,
                True,
            ],
        )
        new_tree.set_scale(0.00001)
        new_tree.rotate_local(90, 0, 0)

        verts = new_tree.vertices
        center = new_tree.center_point

        grass_vertex = grass.vertices[np.random.randint(0, len(grass.vertices))]

        new_tree.move_absolute(
            np.array(grass_vertex) - np.array(get_low_point(verts, center))
        )

        trees.append(new_tree)

        # make a collider for the tree
        collider = renderer.add_object(
            "Cuboid",
            args=[
                np.array([0, 0, 0]),
                np.array([0.25, 0.25, 1]),
                np.array(grass_vertex),
                (255, 0, 0),
            ],
        )

        collider.hide()

        # move collider to the lowest point of the tree
        collider.move_absolute(np.array(grass_vertex) - np.array([0.125, 0.125, 0]))

        tree_colliders.append([collider, True])

    def player_thread():
        while renderer.running:
            # get closest grass vertex to player
            vert_distances = [
                np.linalg.norm(np.array(vert) - np.array(renderer.camera.position))
                for vert in grass.vertices
            ]
            closest_vert = grass.vertices[np.argmin(vert_distances)]

            # move the player to the closest vertex
            renderer.camera.position[2] = closest_vert[2] + 0.2

            sleep(0.05)

    def tree_collide_function():
        for collider in tree_colliders:
            if collider[1]:
                # make 4 points in front of the camera to check for collisions
                points = [
                    renderer.camera.position
                    + np.dot(np.array([0, 0.4, 0]), renderer.camera.rotation_matrix),
                    renderer.camera.position
                    + np.dot(np.array([0, 0.6, 0]), renderer.camera.rotation_matrix),
                    renderer.camera.position
                    + np.dot(np.array([0, 0.8, 0]), renderer.camera.rotation_matrix),
                    renderer.camera.position
                    + np.dot(np.array([0, 1, 0]), renderer.camera.rotation_matrix),
                ]
                for point in points:
                    if collider[0].check_collision(point):
                        # return the index of the tree that was collided with
                        return tree_colliders.index(collider)

    player_thread = Thread(target=player_thread)
    player_thread.start()

    # slowly scale up the trees until they are at .01 scale
    for _ in range(4500):
        for tree in trees:
            tree.set_scale(
                tree.scale + 0.001, get_low_point(tree.vertices, tree.center_point)
            )
        sleep(0.0001)

    pygame_instance = renderer.get_pygame_object()

    # make shop collision box and text
    shop = renderer.add_object(
        "Cuboid",
        args=[
            np.array([0, 0, 0]),
            np.array([0.25, 0.25, 1]),
            np.array([0, 0, 0]),
            (255, 0, 0),
        ],
    )

    renderer.add_object(
        "Text",
        args=[
            "Shop ($100 to half tree cut time)",
            np.array([0.125, 0.125, 0.5]),
            (0, 0, 0),
            0.5,
        ],
    )

    # Define variables to track key press duration and tree look duration
    tree_look_time = 0
    cut_time = 5

    while renderer.running:
        # check if the player clicks
        keys = pygame_instance.key.get_pressed()

        if keys[pygame_instance.K_x]:
            # If the key is pressed, update the key_pressed_time
            if tree_look_time == 0:
                tree_look_time = time()

            # check if the player clicked on a tree
            tree_index = tree_collide_function()
            if tree_index is not None:
                # put percentage of tree cut down to hud as pygame text not renderer
                text = pygame_instance.font.Font(None, 36).render(
                    f"Tree cut down: {round((time() - tree_look_time) / cut_time * 100)}%",
                    True,
                    (0, 0, 0),
                )
                renderer.display.blit(text, (10, 10))

                if time() - tree_look_time >= cut_time:
                    # make thread to cut down tree
                    Thread(
                        target=cut_down_tree,
                        args=(
                            tree_index,
                            renderer,
                            trees,
                            tree_colliders,
                            grass,
                        ),
                    ).start()
                    tree_look_time = 0
                    money += 20
            else:
                tree_look_time = 0

        # If the key is released, reset key_pressed_time and tree_look_time
        if not keys[pygame_instance.K_x]:
            tree_look_time = 0

        # put money to hud as pygame text not renderer
        text = pygame_instance.font.Font(None, 36).render(
            f"Money: {money}", True, (0, 0, 0)
        )
        renderer.display.blit(text, (10, 50))

        # check if the player is in the shop, if so take 100 money and half the tree cut time
        if shop.check_collision(renderer.camera.position):
            if money >= 100:
                money -= 100
                cut_time /= 2

                # change the color of the shop to show it is being used
                shop.color = (0, 255, 0)
        else:
            # change the color of the shop to show it is not being used
            shop.color = (255, 0, 0)

        sleep(0.02)


if __name__ == "__main__":
    main()
