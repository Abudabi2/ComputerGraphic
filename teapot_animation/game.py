import numpy as np
import copy
import task3.geometry.core as core
import matplotlib.pyplot as plt
import task3.load.parse_from_file as prs
from matplotlib.animation import FuncAnimation
import time
import winsound


class Game:
    def __init__(self, pic_size=512):
        self.pic_size = pic_size

        self.def_spike_vertexes = np.array([[-10, 0, 1],
                                            [10, 10, 1],
                                            [10, -10, 1]])

        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("")

        vertexes, self.faces = prs.from_file("teapot_animation\source\small_teapot.obj")
        self.def_vertexes = core.resize(vertexes, 0.1)
        self.cur_x = np.int_(np.round(np.median(self.def_vertexes[:, 0])))
        self.cur_y = np.int_(np.round(np.median(self.def_vertexes[:, 1])))
        self.def_vertexes = core.move(self.def_vertexes, -self.cur_x, -self.cur_y)
        self.start_vertexes = copy.deepcopy(self.def_vertexes)
        self.vertexes = copy.deepcopy(self.def_vertexes)

        self.w = -10
        self.cur_angle = 0
        self.click_count = 0
        self.iteration = 1
        self.finish = False

        self.spike_num = 0

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.img = np.zeros((pic_size, pic_size, 3), dtype=np.uint8)
        self.im = plt.imshow(self.img, animated=True)
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_target,
                                 frames=self.end_game, blit=True, interval=5)

        winsound.PlaySound('teapot_animation\source\sound.wav', winsound.SND_ASYNC | winsound.SND_LOOP)
        self.text = self.ax.text(-100, -40, 'Teapot-747 crashes over the waters of the Atlantic Ocean during {} series'.format(self.iteration - 1))

        plt.show()

    def end_game(self):
        i = 0
        while not self.finish:
            i += 1
            yield i
        if self.finish:
            plt.close()

    def init_target(self, x0=None, y0=None, alpha=None, v0=None):
        self.img = np.zeros((self.pic_size, self.pic_size, 3), dtype=np.uint8)
        self.text.set_text('Teapot-747 crashes over the waters of the Atlantic Ocean during {} series'.format(self.iteration - 1))
        self.fig.canvas.draw()

        if x0 is None:
            self.def_vertexes = copy.deepcopy(self.start_vertexes)
            self.click_count = 0
            self.w = np.random.randint(-30, -10)

            self.spike_num = np.random.randint(2, 4)
            self.spike_vertexes, self.spike_faces = core.create_spike_polygons(self.spike_num)

            x0 = np.ptp(self.def_vertexes[:, 0]) + np.min(self.def_vertexes[:, 0])
        if y0 is None:
            ptp_y = np.int_(np.round(np.ptp(self.def_vertexes[:, 1])))
            y0 = np.random.randint(2 * ptp_y, self.pic_size - ptp_y)
        if alpha is None:
            alpha = np.deg2rad(np.random.randint(-50, -20))
        if v0 is None:
            v0 = np.random.randint(40, 70) + (self.iteration - 1) * 10

        self.vertexes = core.move(self.def_vertexes, x0, y0)

        self.t = time.time()
        self.v0 = v0
        self.x0 = x0
        self.y0 = y0
        self.alpha = alpha

        self.g = 3 * 9.8 + (self.iteration - 1) * 20

        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha)

        return self.im,

    def update(self, par):
        self.img = np.zeros((self.pic_size, self.pic_size, 3), dtype=np.uint8)
        if self.iteration - 1 == 325:
            self.finish = True

        cur_t = time.time() - self.t

        self.cur_x = int(self.x0 + self.v0 * cur_t * np.cos(self.alpha))
        self.cur_y = int(self.y0 + self.v0 * cur_t * np.sin(self.alpha) - self.g * cur_t * cur_t / 2)
        self.cur_angle = (self.cur_angle + self.w) % 360
        self.vertexes = core.move(core.rotate(self.def_vertexes, self.cur_angle), self.cur_x, self.cur_y)

        heat_box_spike_y = 20
        temp = np.ones((self.spike_num, 3))
        for i in range(0, self.spike_num):
            temp[i, 0] = 511
            temp[i, 1] = self.spike_vertexes[3*i, 1]

        spike = False
        for row in self.vertexes:
            for spike_row in temp:
                if 470 < row[0] < 511 and spike_row[1] - heat_box_spike_y < row[1] < spike_row[1]:
                    spike = True

        if np.min(self.vertexes) < 0 or np.max(self.vertexes) >= self.pic_size or spike:
            if np.max(self.vertexes[:, 0]) >= self.pic_size:
                self.iteration += 1
            else:
                self.iteration = 1
            self.init_target()
            return self.im,

        core.polygons(self.vertexes, self.faces, self.img)
        core.polygons(self.spike_vertexes, self.spike_faces, self.img)

        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha) - self.g * cur_t
        if self.w < 0:
            self.w += 0.1

        self.im.set_array(np.rot90(self.img))
        return self.im,

    def onclick(self, event):
        heat_box_x = np.ptp(self.vertexes[:, 0])
        heat_box_y = np.ptp(self.vertexes[:, 1])

        if self.cur_x - heat_box_x < event.xdata < self.cur_x + heat_box_x and \
                self.pic_size - self.cur_y - heat_box_y < event.ydata < self.pic_size - self.cur_y + heat_box_y:

            self.w -= 10
            self.click_count += 1

            if self.click_count == 2:
                self.def_vertexes = core.resize(self.def_vertexes, 1.5)
                self.w = self.w / 2
                self.v0 = self.v0 / 2
                self.click_count = 0

            self.init_target(self.cur_x, self.cur_y, np.deg2rad(45), self.v0 + np.abs(self.vx))


gg = Game()
