import head.tools.transformations_matrices as tm
from head.source.load import from_file
import numpy as np
from PIL import Image


class Model:
    def __init__(self, viewport_size, scale_value, world_coords, view_space_matrix, projection_matrix, projection):
        self.scale_value = scale_value
        self.world_coords = world_coords
        self.viewport_size = viewport_size

        self.world_space = tm.transformation(tm.move(self.world_coords[0], self.world_coords[1], self.world_coords[2]),
                                             tm.roll(90))

        self.vertexes, self.faces, self.texture_vertexes, self.vertexes_normals = from_file("/head/source/face.obj")

        self.vertexes = tm.scale(self.scale_value, self.scale_value, self.scale_value).dot(self.vertexes.T).T

        self.texture = np.asarray(Image.open("/head/source/head.tga"), dtype="int32")

        self.vertexes = tm.transformation(self.world_space, view_space_matrix).dot(self.vertexes.T).T
        self.normals = self.triangle_normals()
        self.vertexes_normals = np.linalg.inv(tm.transformation(self.world_space, view_space_matrix)).T.dot(self.vertexes_normals.T).T

        self.vertexes = projection_matrix.dot(self.vertexes.T).T
        self.to_viewport(projection)

    def to_viewport(self, projection):
        if projection:
            self.vertexes[:, 0] /= -self.vertexes[:, 2]
            self.vertexes[:, 1] /= -self.vertexes[:, 2]

        self.vertexes[:, 0] = ((self.viewport_size - 1) / 2) * self.vertexes[:, 0] + (self.viewport_size - 1) / 2
        self.vertexes[:, 1] = ((self.viewport_size - 1) / 2) * self.vertexes[:, 1] + (self.viewport_size - 1) / 2

    def triangle_normals(self):
        norm = np.zeros((np.size(self.faces[:, 0, 0]), 3))
        for i, (x0, y0, z0, x1, y1, z1, x2, y2, z2) in enumerate(
                zip(self.vertexes[self.faces[:, 0, 0] - 1, 0], self.vertexes[self.faces[:, 0, 0] - 1, 1],
                    self.vertexes[self.faces[:, 0, 0] - 1, 2],

                    self.vertexes[self.faces[:, 1, 0] - 1, 0], self.vertexes[self.faces[:, 1, 0] - 1, 1],
                    self.vertexes[self.faces[:, 1, 0] - 1, 2],

                    self.vertexes[self.faces[:, 2, 0] - 1, 0], self.vertexes[self.faces[:, 2, 0] - 1, 1],
                    self.vertexes[self.faces[:, 2, 0] - 1, 2])):
            norm[i] = np.cross([x1 - x0, y1 - y0, z1 - z0], [x2 - x0, y2 - y0, z2 - z0])
        return norm
