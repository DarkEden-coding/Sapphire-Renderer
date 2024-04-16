import numpy as np


def average_points(points):
    """
    Averages a list of points
    :param points: list of points
    :return: average point
    """
    return np.mean(points, axis=0, dtype=float)
