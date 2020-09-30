import numpy as np
import matplotlib.pyplot as plt


def line(x0, y0, x1, y1, image):
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
            image[y0, x] += True
        else:
            image[x, y0] += True
        error += k
        if error >= delta_x:
            y0 += delta_y
            error -= delta_x << 1


def prepare_image(pic_size):
    return np.zeros(shape=(pic_size, pic_size)).astype(np.uint8)


def show_image(image):
    plt.imshow(image.T, cmap="gray")
    plt.show()


size = 512
img = prepare_image(size)
X0, Y0, X1, Y1 = 0, 0, 500, 250
line(X0, Y0, X1, Y1, img)
show_image(img)
