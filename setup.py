from setuptools import setup, find_packages

long_description = """
# Sapphire Renderer

Sapphire Renderer is a Python package that allows you to easily render simple 3D scenes. It provides a set of classes and functions to create and manipulate 3D objects, and to render them in a window.

## Features

- **3D Object Creation**: Sapphire Renderer provides classes to create various 3D objects such as Torus, VertLineObject, etc. You can also create your own custom objects.

- **Camera Control**: The package includes a Camera class that allows you to control the viewpoint from which the scene is rendered. You can move and rotate the camera in the 3D space.

- **Object Manipulation**: You can add, remove, and update objects in the scene.

- **Rendering**: The package provides a main rendering loop that continuously updates and renders the scene.

## Installation

You can install Sapphire Renderer using pip:

```bash
pip install sapphire-renderer
```

## Basic Usage

Here is a basic example of how to use Sapphire Renderer:

```python
from sapphirerenderer import SapphireRenderer

# Create a renderer
renderer = SapphireRenderer(width=1000, height=1000, draw_axis=True)

# Add a Torus object to the scene
renderer.add_object("Torus")

# Start the rendering loop
renderer.render_loop()
```

In this example, we first create a SapphireRenderer instance. We then add a Torus object to the scene. Finally, we start the rendering loop which will continuously update and render the scene.

## Documentation

For more detailed information on how to use Sapphire Renderer, please refer to the [official documentation](https://github.com/DarkEden-coding/Sapphire-Renderer)(WIP).

## License

Sapphire Renderer is licensed under the MIT License."""

install_requires = [
    "numpy",
    "numba",
    "pygame",
    "setuptools",
    "pywavefront",
    "numpy-stl",
]

setup(
    name="sapphire-renderer",
    version="0.0.49",
    author="Dark_Eden",
    author_email="darkedenc9@gmail.com",
    description="A package to easily render simple 3D scenes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DarkEden-coding/Sapphire-Renderer",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
