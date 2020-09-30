from input_data.read import from_file
from geometry.parse_data import scale_vertexes, create_pixels_field
from visualize.plot import show_image

vertexes, faces = from_file("teapot/input_data/task1.obj")
scaled_vertexes = scale_vertexes(vertexes)

show_image(create_pixels_field(512, scaled_vertexes, faces))