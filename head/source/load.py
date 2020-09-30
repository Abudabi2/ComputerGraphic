import numpy as np


def from_file(filename):
    data = np.loadtxt(filename, dtype='U')
    vertexes, faces, texture_vertexes, vertexes_normals = \
        get_vertexes(data, "v"), get_faces(data), get_vertexes(data, "vt"), get_vertexes(data, "vn")
    return vertexes, faces, texture_vertexes, vertexes_normals


def get_vertexes(inp_data, v_type):
    vertexes = (inp_data[inp_data[:, 0] == v_type])[:, 1:4].astype(np.float_)
    vertexes = np.append(vertexes, np.ones([np.size(vertexes[:, 0]), 1]), 1)
    return vertexes


def get_faces(inp_data):
    faces = ((inp_data[inp_data[:, 0] == "f"])[:, 1:4])
    temp = np.zeros((faces[:, 0].size, 3, 3))

    faces = np.char.split(np.char.replace(faces, '/', ' '))

    for i, j in zip(temp[:, :], faces[:, :]):
        i[0], i[1], i[2] = j[0], j[1], j[2]

    return np.int_(temp)
