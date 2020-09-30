import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
from time import monotonic as timer
from time import sleep


class Digits:

    digits =\
        np.array([
                  # zero
                  [[231.0, 75.0], [365.0, 81.0], [369.0, 201.0],
                   [369.0, 275.0], [369.0, 349.0], [345.0, 447.0],
                   [256.0, 446.0], [167.0, 445.0], [139.0, 358.0],
                   [131.0, 258.0], [123.0, 158.0], [159.0, 84.0],
                   [254, 47]],
                  # one
                  [[255.0, 424.0], [254.0, 361.0], [256.0, 412.0],
                   [255.0, 303.0],  [254.0, 194.0], [254.0, 234.0],
                   [253.0, 167.0], [252.0, 100.0], [256.0, 28.0],
                   [243.0, 43.0], [230.0, 58.0], [226.0, 99.0],
                   [138.0, 180.0]],
                  # two
                  [[373.0, 414.0], [327.0, 393.0], [104.0, 356.0],
                   [120.0, 405.0], [136.0, 454.0], [312.0, 323.0],
                   [336.0, 241.0], [360.0, 159.0], [334.0, 74.0],
                   [271.0, 50.0], [208.0, 26.0], [152.0, 55.0],
                   [104.0, 111.0]],
                  # three
                  [[93.0, 391.0], [110.0, 445.0], [280.0, 503.0],
                   [338.0, 388.0], [396.0, 273.0], [174.0, 215.0],
                   [182.0, 250.0], [190.0, 285.0], [355.0, 197.0],
                   [311.0, 107.0], [267.0, 17.0], [113.0, 14.0],
                   [96.0, 132.0]],
                  # four
                  [[247.0, 438.0], [246.0, 435.0], [237.0, 246.0],
                   [260.0, 108.0], [283.0, -30.0], [242.0, 30.0],
                   [192.0, 84.0], [142.0, 138.0], [70.0, 244.0],
                   [131.0, 239.0], [192.0, 234.0], [249.0, 230.0],
                   [374.0, 244.0]],
                  # five
                  [[147.0, 409.0], [262.0, 452.0], [371.0, 439.0],
                   [361.0, 302.0], [351.0, 165.0], [159.0, 243.0],
                   [152.0, 223.0], [145.0, 203.0], [135.0, 78.0],
                   [144.0, 61.0], [153.0, 44.0], [226.0, 42.0],
                   [340.0, 52.0]],
                  # six
                  [[168.0, 285.0], [220.0, 243.0], [329.0, 240.0],
                   [348.0, 321.0], [367.0, 402.0], [321.0, 465.0],
                   [242.0, 458.0], [163.0, 451.0], [138.0, 368.0],
                   [149.0, 296.0], [160.0, 224.0], [191.0, 104.0],
                   [301.0, 26.0]],
                  # seven
                  [[198.0, 452.0], [200.0, 388.0], [219.0, 323.0],
                   [231.0, 295.0], [243.0, 267.0], [283.0, 187.0],
                   [294.0, 166.0], [305.0, 145.0], [379.0, 34.0],
                   [312.0, 38.0], [245.0, 42.0], [168.0, 34.0],
                   [108.0, 52.0]],
                  # eight
                  [[217.0, 255.0], [124.0, 304.0], [93.0, 437.0],
                   [248.0, 432.0], [403.0, 427.0], [307.0, 279.0],
                   [225.0, 247.0], [143.0, 215.0], [127.0, 34.0],
                   [240.0, 43.0], [353.0, 52.0], [336.0, 184.0],
                   [243.0, 242.0]],
                  # nine
                  [[297.0, 448.0], [297.0, 365.0], [298.0, 95.0],
                   [322.0, 122.0], [346.0, 149.0], [277.0, 196.0],
                   [219.0, 190.0], [161.0, 184.0], [131.0, 137.0],
                   [151.0, 85.0], [171.0, 33.0], [323.0, 6.0],
                   [322.0, 105.0]]])

    def get_coords(self, cur_digits):
        digits = np.zeros([6, 13, 2])
        for enum, digit in enumerate(cur_digits):
            digits[enum] = self.digits[digit]
        return digits


def get_cur_time():
    return np.array([datetime.now().hour // 10, datetime.now().hour % 10,
                    datetime.now().minute // 10, datetime.now().minute % 10,
                    datetime.now().second // 10, datetime.now().second % 10], dtype=int)


class Clock:

    def __init__(self, digits_fps=5):
        self.anim_speed = digits_fps + 1
        self.finish = False
        self.Digits = Digits()
        self.digit_max_value = [3, 5, 6, 10, 6, 10]
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Clock")
        self.img = np.zeros((512, 3000, 3), dtype=np.uint8)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.im = plt.imshow(self.img, animated=True)
        self.start_plot()
        self.ani = FuncAnimation(self.fig, self.plot_digit, init_func=self.init_anim,
                                 frames=self.end_clock, blit=True, interval=5)
        plt.show()

    def end_clock(self):
        ii = 0
        while not self.finish:
            ii += 1
            yield ii

    def init_anim(self, digits=get_cur_time(), iter_started=False):
        try:
            self.interval = timer() - self.start
            if iter_started and abs(self.iter_time - self.interval) > 0.05:
                self.anim_speed = int(self.anim_speed / self.interval)
            if timer() - self.start < self.iter_time:
                sleep(self.iter_time - timer() + self.start)
            self.start = timer()
        except:
            self.start = timer()
            self.iter_time = 1

        self.cur_digit = digits
        self.digit_to_change = self.calc_digit_to_change()
        self.cur_step = 0
        self.vertexes_points = self.Digits.get_coords(self.cur_digit)
        self.step_to_shift = ((self.Digits.digits[(self.cur_digit + 1) % self.digit_max_value] -
                               self.Digits.digits[self.cur_digit]) / (self.anim_speed - 1))

        return self.im,

    def onclick(self, event):
        self.finish = not self.finish

    def bezier(self, x, y, t_step, d_num):
        vertexes = np.zeros((np.int_(1 // t_step + 1), 2), dtype=int)

        for count, t in enumerate(np.arange(0, 1, t_step)):
            vertexes[count, 0], vertexes[count, 1] = self.casteljau(x, y, t)

        vertexes[:, 0] += d_num * 500

        np.vectorize(lambda x0, y0, x1, y1: self.line(x0, y0, x1, y1))(
            vertexes[1:, 0], vertexes[1:, 1],
            vertexes[:(np.size(vertexes[:, 0]) - 1), 0], vertexes[:(np.size(vertexes[:, 0]) - 1), 1])

    def casteljau(self, x, y, t):
        if np.size(x) == 1:
            return int(x[0]), int(y[0])
        else:
            return self.casteljau(x[1:] * (1 - t) + x[:np.size(x) - 1] * t,
                                  y[1:] * (1 - t) + y[:np.size(y) - 1] * t, t)

    def line(self, x0, y0, x1, y1):
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
                self.img[x, y0] = (255, 255, 255)
            else:
                self.img[y0, x] = (255, 255, 255)
            error += k
            if error >= delta_x:
                y0 += delta_y
                error -= delta_x << 1

    def plot_digit(self, par):
        if self.cur_step == self.anim_speed:
            self.digit_max_value[1] = 5 if self.digit_max_value[0] == 2 else 10

            self.digit_to_change = self.calc_digit_to_change()

            self.cur_digit[self.digit_to_change:] += 1
            self.init_anim(self.cur_digit % self.digit_max_value, True)
            return self.im,
        else:
            self.img[:, self.digit_to_change * 500:] = 0
            for offset in range(self.digit_to_change, 6):
                for i in range(0, np.size(self.vertexes_points[offset, :, 0]) - 1, 3):
                    self.bezier(
                      self.vertexes_points[offset, i:i + 4, 0] + self.step_to_shift[offset, i:i + 4, 0] * self.cur_step,
                      self.vertexes_points[offset, i:i + 4, 1] + self.step_to_shift[offset, i:i + 4, 1] * self.cur_step,
                      0.1, offset)
            self.im.set_array(self.img)
            self.cur_step += 1
            return self.im,

    def start_plot(self):
        self.cur_digit = get_cur_time()
        self.vertexes_points = self.Digits.get_coords(self.cur_digit)
        for offset in range(0, 6):
            for i in range(0, np.size(self.vertexes_points[offset, :, 0]) - 1, 3):
                self.bezier(self.vertexes_points[offset, i:i + 4, 0],
                            self.vertexes_points[offset, i:i + 4, 1],
                            0.01, offset)

    def calc_digit_to_change(self):
        digit_to_change = 5
        for digit, max_value in zip(np.flip(self.cur_digit), np.flip(self.digit_max_value)):
            if digit + 1 == max_value:
                digit_to_change -= 1
                if digit_to_change < 0:
                    digit_to_change = 0
            else:
                break
        return digit_to_change


clock = Clock()
