import numpy as np


def get_pitch_matrix(yaw):
    return np.array(
        [[np.cos(yaw), 0, np.sin(yaw)], [0, 1, 0], [-np.sin(yaw), 0, np.cos(yaw)]]
    )


def get_roll_matrix(pitch):
    return np.array(
        [
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)],
        ]
    )


def get_yaw_matrix(roll):
    return np.array(
        [[np.cos(roll), -np.sin(roll), 0], [np.sin(roll), np.cos(roll), 0], [0, 0, 1]]
    )


def get_pitch_yaw_matrix(pitch, yaw):
    return np.dot(get_roll_matrix(pitch), get_yaw_matrix(yaw))


def get_pitch_yaw_roll_matrix(yaw, pitch, roll):
    return np.dot(get_pitch_yaw_matrix(yaw, pitch), get_pitch_matrix(roll))
