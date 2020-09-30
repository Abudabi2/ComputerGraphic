import numpy as np


def resize(vertexes, koef):
    resize_matrix = np.array(([koef, 0, 0],
                              [0, koef, 0],
                              [0, 0, 1]))
    vertexes = resize_matrix.dot(vertexes.T).T
    vertexes = np.int_(np.round_(vertexes))
    return vertexes


def polygons(vertexes, faces, pixels):
    draw_polygons = np.vectorize(lambda x0, y0, x1, y1, x2, y2: (color(x0, y0, x1, y1, x2, y2, pixels)))
    draw_polygons(vertexes[faces[:, 0] - 1, 0], vertexes[faces[:, 0] - 1, 1],
                  vertexes[faces[:, 1] - 1, 0], vertexes[faces[:, 1] - 1, 1],
                  vertexes[faces[:, 2] - 1, 0], vertexes[faces[:, 2] - 1, 1])


def color(x0, y0, x1, y1, x2, y2, pixels):
    pol_shade = (x0*y0 + x1*y1 + x2*y2) % 255
    pol_color = pol_shade % 3

    y_min = min(y0, y1, y2)
    y_max = max(y0, y1, y2)
    x_min = min(x0, x1, x2)
    x_max = max(x0, x1, x2)

    x = [x1 - x0, x2 - x0, 0]
    y = [y1 - y0, y2 - y0, 0]
    res2 = x[0] * y[1] - x[1] * y[0]

    if res2 == 0:
        return

    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            x[2] = x0 - i
            y[2] = y0 - j

            b = (x[1] * y[2] - x[2] * y[1]) / res2
            c = (x[2] * y[0] - x[0] * y[2]) / res2

            if b + c <= 1 and b >= 0 and c >= 0:
                pixels[i, j, pol_color] += pol_shade


def rotate(vertexes, angle):
    cosf = np.cos((angle*np.pi)/180)
    sinf = np.sin((angle*np.pi)/180)
    rotate_matrix = np.array(([cosf, -sinf, 0],
                              [sinf, cosf,  0],
                              [0,    0,     1]))
    vertexes = np.int_(np.round(rotate_matrix.dot(vertexes.T)).T)
    return vertexes


def move(vertexes, x0, y0):
    move_matrix = np.array(([1, 0, x0],
                            [0, 1, y0],
                            [0, 0, 1]))
    return (move_matrix.dot(vertexes.T)).T


def create_spike_polygons(spike_num):
    vertexes = np.ones((spike_num*3, 3))
    faces = np.zeros((spike_num, 3))

    for i in range(0, spike_num):
        y = np.random.randint(20, 490)

        vertexes[i * 3, 0] = 470
        vertexes[i * 3 + 1, 0] = 511
        vertexes[i * 3 + 2, 0] = 511

        vertexes[i*3, 1] = y
        vertexes[i*3 + 1, 1] = y - 20
        vertexes[i*3 + 2, 1] = y + 20

        faces[i, 0] = i*3 + 1
        faces[i, 1] = i*3 + 2
        faces[i, 2] = i*3 + 3
    return np.int_(vertexes), np.int_(faces)



