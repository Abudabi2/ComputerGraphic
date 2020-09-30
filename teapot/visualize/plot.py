from matplotlib.pyplot import imshow, show


def show_image(image):
    imshow(image.T, cmap="gray")
    show()
