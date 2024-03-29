from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read().splitlines()

setup(
    name="sapphire-renderer",
    version="0.0.18",
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
