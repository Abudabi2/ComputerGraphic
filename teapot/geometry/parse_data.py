import numpy as np


def create_pixels_field(pic_size, vertexes, faces):
    pixels = np.zeros((pic_size, pic_size), dtype=bool)
    polygons(vertexes, faces, pixels)
    pixels = np.fliplr(pixels)
    return pixels


def polygons(vertexes, faces, pixels):
    for x0, y0, x1, y1, x2, y2 in zip(vertexes[faces[:, 0] - 1, 0], vertexes[faces[:, 0] - 1, 1],
                                      vertexes[faces[:, 1] - 1, 0], vertexes[faces[:, 1] - 1, 1],
                                      vertexes[faces[:, 2] - 1, 0], vertexes[faces[:, 2] - 1, 1]):
        line(x0, y0, x1, y1, pixels)
        line(x1, y1, x2, y2, pixels)
        line(x2, y2, x0, y0, pixels)


def line(x0, y0, x1, y1, pixels):
    steep = False

    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    k = abs(y1 - y0) << 1
    delta_x = x1 - x0
    error = 0
    delta_y = 1 if y1 > y0 else -1

    for x in range(x0, x1 + 1):
        if steep:
            pixels[y0, x] += True
        else:
            pixels[x, y0] += True
        error += k
        if error >= delta_x:
            y0 += delta_y
            error -= delta_x << 1
    return


def scale_vertexes(vertexes):
    to_axis_start(vertexes)
    scale_k = 511 / max(np.ptp(vertexes[:, 0]), np.ptp(vertexes[:, 1]))
    vertexes *= scale_k
    vertexes = np.int_(np.round_(vertexes))
    return vertexes


def to_axis_start(vertexes):
    min0 = min(vertexes[:, 0])
    min1 = min(vertexes[:, 1])
    if min0 != 0:
        vertexes[:, 0] -= min0
    if min1 != 0:
        vertexes[:, 1] -= min1

