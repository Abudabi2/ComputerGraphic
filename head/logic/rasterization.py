import numpy as np


def normalize(vector):
    vector_norm = np.linalg.norm(vector)
    if vector_norm == 0:
        vector_norm = 1
    return vector/vector_norm


class Rasterization:
    def __init__(self, light_source, enables, viewport_size, texture, vertexes, faces, texture_vertexes, vertexes_normals, normals, i_d, i_s, alpha, view):
        self.enable_bfc, self.enable_zbuff, self.enable_fong_model, self.enable_textures = \
            enables[0], enables[1], enables[2], enables[3]

        self.light_source = normalize(light_source)
        self.viewport_size = viewport_size
        self.zbuff = np.full((viewport_size, viewport_size), np.inf)
        self.texture = texture

        self.vertexes, self.faces, self.texture_vertexes, self.vertexes_normals, self.normals = \
            np.int_(np.round(vertexes)), faces, texture_vertexes, vertexes_normals, normals

        self.img = np.zeros((viewport_size, viewport_size, 3))

        self.i_d = i_d
        self.i_s = i_s
        self.shine = normalize(self.light_source + view)
        self.alpha = alpha

        if self.enable_fong_model:
            if self.enable_textures:
                self.polygons_fong_texture()
            else:
                self.polygons_fong()
        else:
            if self.enable_textures:
                self.polygons_lambert_texture()
            else:
                self.polygons_lambert()

    def shine_value(self, v):
        shine = v.dot(self.shine)
        if shine < 0:
            shine = 0
        return shine


    def light_value(self, v):
        v = normalize(v)

        if self.enable_bfc:
            if v.dot([0, 0, -1]) > 0:
                return -1

        light = v.dot(self.light_source)
        if light <= 0:
            return 0

        return light

    def polygons_lambert(self):
        for x0, y0, z0, x1, y1, z1, x2, y2, z2, n0, n1, n2 in \
                      zip(self.vertexes[self.faces[:, 0, 0] - 1, 0], self.vertexes[self.faces[:, 0, 0] - 1, 1], self.vertexes[self.faces[:, 0, 0] - 1, 2],
                          self.vertexes[self.faces[:, 1, 0] - 1, 0], self.vertexes[self.faces[:, 1, 0] - 1, 1], self.vertexes[self.faces[:, 1, 0] - 1, 2],
                          self.vertexes[self.faces[:, 2, 0] - 1, 0], self.vertexes[self.faces[:, 2, 0] - 1, 1], self.vertexes[self.faces[:, 2, 0] - 1, 2],
                          self.normals[:, 0],  self.normals[:, 1],  self.normals[:, 2]):
            light = self.light_value([n0, n1, n2])

            if light != -1:
                self.draw_polygon([x0, y0, z0], [x1, y1, z1], [x2, y2, z2], light)

    def polygons_lambert_texture(self):
        for x0, y0, z0, x1, y1, z1, x2, y2, z2, t00, t01, t02, t10, t11, t12, t20, t21, t22, n0, n1, n2 in \
                      zip(self.vertexes[self.faces[:, 0, 0] - 1, 0], self.vertexes[self.faces[:, 0, 0] - 1, 1], self.vertexes[self.faces[:, 0, 0] - 1, 2],
                          self.vertexes[self.faces[:, 1, 0] - 1, 0], self.vertexes[self.faces[:, 1, 0] - 1, 1], self.vertexes[self.faces[:, 1, 0] - 1, 2],
                          self.vertexes[self.faces[:, 2, 0] - 1, 0], self.vertexes[self.faces[:, 2, 0] - 1, 1], self.vertexes[self.faces[:, 2, 0] - 1, 2],
                          self.texture_vertexes[self.faces[:, 0, 1] - 1, 0], self.texture_vertexes[self.faces[:, 0, 1] - 1, 1], self.texture_vertexes[self.faces[:, 0, 1] - 1, 2],
                          self.texture_vertexes[self.faces[:, 1, 1] - 1, 0], self.texture_vertexes[self.faces[:, 1, 1] - 1, 1], self.texture_vertexes[self.faces[:, 1, 1] - 1, 2],
                          self.texture_vertexes[self.faces[:, 2, 1] - 1, 0], self.texture_vertexes[self.faces[:, 2, 1] - 1, 1], self.texture_vertexes[self.faces[:, 2, 1] - 1, 2],
                          self.normals[:, 0],  self.normals[:, 1],  self.normals[:, 2]):
            light = self.light_value([n0, n1, n2])

            if light != -1:
                self.draw_polygon([x0, y0, z0], [x1, y1, z1], [x2, y2, z2], light, None, None, None, [t00, t01, t02], [t10, t11, t12], [t20, t21, t22])

    def polygons_fong(self):
        for x0, y0, z0, x1, y1, z1, x2, y2, z2, n00, n01, n02, n10, n11, n12, n20, n21, n22, norm0, norm1, norm2 in \
                      zip(self.vertexes[self.faces[:, 0, 0] - 1, 0], self.vertexes[self.faces[:, 0, 0] - 1, 1], self.vertexes[self.faces[:, 0, 0] - 1, 2],
                          self.vertexes[self.faces[:, 1, 0] - 1, 0], self.vertexes[self.faces[:, 1, 0] - 1, 1], self.vertexes[self.faces[:, 1, 0] - 1, 2],
                          self.vertexes[self.faces[:, 2, 0] - 1, 0], self.vertexes[self.faces[:, 2, 0] - 1, 1], self.vertexes[self.faces[:, 2, 0] - 1, 2],
                          self.vertexes_normals[self.faces[:, 0, 2] - 1, 0],  self.vertexes_normals[self.faces[:, 0, 2] - 1, 1],  self.vertexes_normals[self.faces[:, 0, 2] - 1, 2],
                          self.vertexes_normals[self.faces[:, 1, 2] - 1, 0],  self.vertexes_normals[self.faces[:, 1, 2] - 1, 1],  self.vertexes_normals[self.faces[:, 1, 2] - 1, 2],
                          self.vertexes_normals[self.faces[:, 2, 2] - 1, 0],  self.vertexes_normals[self.faces[:, 2, 2] - 1, 1],  self.vertexes_normals[self.faces[:, 2, 2] - 1, 2],
                          self.normals[:, 0],  self.normals[:, 1],  self.normals[:, 2]):
            light = self.light_value([norm0, norm1, norm2])

            if light != -1:
                self.draw_polygon([x0, y0, z0], [x1, y1, z1], [x2, y2, z2], light, [n00, n01, n02], [n10, n11, n12], [n20, n21, n22])

    def polygons_fong_texture(self):
        for x0, y0, z0, x1, y1, z1, x2, y2, z2, n00, n01, n02, n10, n11, n12, n20, n21, n22, t00, t01, t02, t10, t11, t12, t20, t21, t22,  norm0, norm1, norm2 in \
                      zip(self.vertexes[self.faces[:, 0, 0] - 1, 0], self.vertexes[self.faces[:, 0, 0] - 1, 1], self.vertexes[self.faces[:, 0, 0] - 1, 2],
                          self.vertexes[self.faces[:, 1, 0] - 1, 0], self.vertexes[self.faces[:, 1, 0] - 1, 1], self.vertexes[self.faces[:, 1, 0] - 1, 2],
                          self.vertexes[self.faces[:, 2, 0] - 1, 0], self.vertexes[self.faces[:, 2, 0] - 1, 1], self.vertexes[self.faces[:, 2, 0] - 1, 2],
                          self.vertexes_normals[self.faces[:, 0, 2] - 1, 0], self.vertexes_normals[self.faces[:, 0, 2] - 1, 1], self.vertexes_normals[self.faces[:, 0, 2] - 1, 2],
                          self.vertexes_normals[self.faces[:, 1, 2] - 1, 0], self.vertexes_normals[self.faces[:, 1, 2] - 1, 1], self.vertexes_normals[self.faces[:, 1, 2] - 1, 2],
                          self.vertexes_normals[self.faces[:, 2, 2] - 1, 0], self.vertexes_normals[self.faces[:, 2, 2] - 1, 1], self.vertexes_normals[self.faces[:, 2, 2] - 1, 2],
                          self.texture_vertexes[self.faces[:, 0, 1] - 1, 0], self.texture_vertexes[self.faces[:, 0, 1] - 1, 1], self.texture_vertexes[self.faces[:, 0, 1] - 1, 2],
                          self.texture_vertexes[self.faces[:, 1, 1] - 1, 0], self.texture_vertexes[self.faces[:, 1, 1] - 1, 1], self.texture_vertexes[self.faces[:, 1, 1] - 1, 2],
                          self.texture_vertexes[self.faces[:, 2, 1] - 1, 0], self.texture_vertexes[self.faces[:, 2, 1] - 1, 1], self.texture_vertexes[self.faces[:, 2, 1] - 1, 2],
                          self.normals[:, 0],  self.normals[:, 1],  self.normals[:, 2]):
            light = self.light_value([norm0, norm1, norm2]) * self.i_d

            if light != -1:
                self.draw_polygon([x0, y0, z0], [x1, y1, z1], [x2, y2, z2], light, [n00, n01, n02], [n10, n11, n12], [n20, n21, n22], [t00, t01, t02], [t10, t11, t12], [t20, t21, t22])

    def draw_polygon(self, p0, p1, p2, light, np0=None, np1=None, np2=None, tp0=None, tp1=None, tp2=None):
        y_min = min(p0[1], p1[1], p2[1])
        y_max = max(p0[1], p1[1], p2[1])
        x_min = min(p0[0], p1[0], p2[0])
        x_max = max(p0[0], p1[0], p2[0])

        x = [p1[0] - p0[0], p2[0] - p0[0], 0]
        y = [p1[1] - p0[1], p2[1] - p0[1], 0]
        res2 = x[0] * y[1] - x[1] * y[0]

        if res2 == 0:
            return

        t1 = p0[0] - x_min + 1
        t2 = p0[1] - y_min + 1
        t3 = y_max + 1 - y_min

        b = x[1] * t2 - t1 * y[1]
        c = t1 * y[0] - x[0] * t2

        for i in range(x_min, x_max + 1):
            b += y[1]
            c -= y[0]

            for j in range(y_min, y_max + 1):
                b -= x[1]
                c += x[0]
                res_b = b / res2
                res_c = c / res2
                res_a = 1 - res_b - res_c

                if 0 < i < self.viewport_size and 0 < j < self.viewport_size:
                    if res_a >= 0 and res_b >= 0 and res_c >= 0:
                        if self.enable_fong_model:
                            n_int = np.array([res_a * np0[0] + res_b * np1[0] + res_c * np2[0],
                                              res_a * np0[1] + res_b * np1[1] + res_c * np2[1],
                                              res_a * np0[2] + res_b * np1[2] + res_c * np2[2]])
                            light = self.light_value(n_int) * self.i_d + self.shine_value(n_int)**self.alpha * self.i_s
                        if light != 0:
                            if self.enable_textures:
                                t_int = [res_a * tp0[0] + res_b * tp1[0] + res_c * tp2[0],
                                         res_a * tp0[1] + res_b * tp1[1] + res_c * tp2[1]]
                                color = self.texture[np.int_(np.round((1 - t_int[1]) * 1023)), np.int_(np.round(t_int[0] * 1023))] * light
                            else:
                                color = [light*255, light*255, light*255]
                            if self.enable_zbuff:
                                z = res_a * p0[2] + res_b * p1[2] + res_c * p2[2]
                                if z < self.zbuff[i, j]:
                                    self.zbuff[i, j] = z
                                    self.img[i, j, :] = color
                            else:
                                self.img[i, j, :] = color

            b += x[1] * t3
            c -= x[0] * t3
