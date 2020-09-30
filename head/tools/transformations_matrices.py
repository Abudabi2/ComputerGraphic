import numpy as np


def move(x, y, z):
    return np.array(([1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]))


def scale(x_koef, y_koef, z_koef):
    return np.array(([x_koef, 0,      0,      0],
                     [0,      y_koef, 0,      0],
                     [0,      0,      z_koef, 0],
                     [0,      0,      0,      1]))


def pitch(angle):                    # тангаж, поворот вокруг x
    cosf = np.cos((angle * np.pi) / 180)
    sinf = np.sin((angle * np.pi) / 180)

    return np.array(([1, 0,    0,     0],
                     [0, cosf, -sinf, 0],
                     [0, sinf, cosf,  0],
                     [0, 0,    0,     1]))


def yaw(angle):                      # рыск, поворот вокруг y
    cosf = np.cos((angle * np.pi) / 180)
    sinf = np.sin((angle * np.pi) / 180)

    return np.array(([cosf, 0, -sinf, 0],
                     [0,    1, 0,     0],
                     [sinf, 0, cosf,  0],
                     [0,    0, 0,     1]))


def roll(angle):                      # качение, поворот вокруг z
    cosf = np.cos((angle * np.pi) / 180)
    sinf = np.sin((angle * np.pi) / 180)

    return np.array(([cosf, -sinf, 0, 0],
                     [sinf, cosf, 0,  0],
                     [0,    0,    1,  0],
                     [0,    0,    0,  1]))


def look_at_rotate(look_from, look_to):
    forward = (look_from - look_to)/np.linalg.norm(look_from - look_to)
    right = np.cross([0, 1, 0], forward)/np.linalg.norm(np.cross([0, 1, 0], forward))
    up = np.cross(forward, right)/np.linalg.norm(np.cross(forward, right))
    return np.array(([right[0],   right[1],   right[2],    0],
                     [up[0],      up[1],      up[2],       0],
                     [forward[0], forward[1], forward[2],  0],
                     [0,          0,          0,           1]))


def orthographic(t, b, r, l, f, n):
    return np.array(([2 / (r - l), 0,           0,            -(r + l) / (r - l)],
                     [0,           2 / (t - b), 0,            -(t + b) / (t - b)],
                     [0,           0,           -2 / (f - n), -(f + n) / (f - n)],
                     [0,           0,           0,                             1]))


def perspective(t, b, r, l, f, n):
    return np.array(([2 * n / (r - l), 0,               (r + l) / (r - l),                        0],
                     [0,               2 * n / (t - b), (t + b) / (t - b),                        0],
                     [0,               0,               -(f + n) / (f - n), - (2 * f * n / (f - n))],
                     [0,               0,               -1,                                       0]))


def transformation(*matrices):
    ret_matrix = np.array(([1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]))

    for matrix in matrices:
        ret_matrix = ret_matrix.dot(matrix)

    return ret_matrix
