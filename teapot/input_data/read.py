from numpy import loadtxt, float_, int_


def from_file(filename):
    data = loadtxt(filename, dtype='U', delimiter=' ')
    vertexes, faces = get_vertexes(data), get_faces(data)
    return vertexes, faces


def get_vertexes(inp_data):
    mask = inp_data[:, 0] == 'v'
    vertexes = inp_data[:, 1:3].astype(float_)
    return vertexes[mask]


def get_faces(inp_data):
    mask = inp_data[:, 0] == 'f'
    faces = inp_data[:, 1:4].astype(float_)
    return int_(faces[mask])
