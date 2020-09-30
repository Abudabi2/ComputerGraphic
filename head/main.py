from head.logic.camera import Camera
from head.logic.model import Model
from head.logic.rasterization import Rasterization
from matplotlib.pyplot import imshow, show
import numpy as np


enable_perspective_projection = True           # False = orthographic    |  True = perspective
enable_bfc = True
enable_zbuff = True
enable_fong_model = True                       # False = Lambert model   |  True = Fong model
enable_textures = False

light_source = [0, 0, 1]
viewport = 1000
scale = 50
world = [50, 50, 150]
t, b, r, l, f, n = 100, 0, 100, 0, 400, -250
look_from, look_to = np.array([0, 0, 0]), np.array([0, 10, -150])

i_d = 1
i_s = 0
alpha = 10

enables = [enable_bfc, enable_zbuff, enable_fong_model, enable_textures]

camera = Camera(look_from, look_to, t, b, r, l, f, n, enable_perspective_projection)

model = Model(viewport, scale, world, camera.view_space, camera.projection, enable_perspective_projection)

img = Rasterization(light_source, enables, model.viewport_size, model.texture, model.vertexes, model.faces,
                    model.texture_vertexes, model.vertexes_normals, model.normals, i_d, i_s, alpha, look_from - look_to).img
imshow(np.int_(img))
show()
