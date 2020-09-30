import numpy as np


def from_file(filename):
    data = np.loadtxt(filename, dtype='U', delimiter=' ')
    vertexes, faces = get_vertexes(data), get_faces(data)
    return vertexes, faces


def get_vertexes(inp_data):
    vertexes = (inp_data[inp_data[:, 0] == 'v'])[:, 1:3].astype(np.float_)
    vertexes = np.append(vertexes, np.ones([np.size(vertexes[:, 0]), 1]), 1)
    return vertexes


def get_faces(inp_data):
    faces = ((inp_data[inp_data[:, 0] == 'f'])[:, 1:4])
    faces = np.char.replace(faces, '/0/0', '')
    return np.int_(faces)
