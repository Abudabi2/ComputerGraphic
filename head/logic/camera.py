import head.tools.transformations_matrices as tm
import numpy as np


class Camera:
    def __init__(self, look_from, look_to, t, b, r, l, f, n, projection):
        self.look_from, self.look_to = np.array(look_from), np.array(look_to)
        self.top, self.bot, self.right, self.left, self.far, self.near = t, b, r, l, f, n

        self.view_space = tm.transformation(tm.look_at_rotate(self.look_from, self.look_to),
                                            tm.move(-self.look_from[0], -self.look_from[1], -self.look_from[2]))
        self.projection = tm.perspective(self.top, self.bot, self.right, self.left, self.far, self.near) if projection \
            else tm.orthographic(self.top, self.bot, self.right, self.left, -self.far, -self.near)
