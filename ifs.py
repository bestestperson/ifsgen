import numpy as np
import random
import math
import PIL
from PIL import Image, ImageColor

class ifs:

    def __init__ (self):
        self.data = np.array([])
        self.coords = np.array([])

    def getData(self, fileName = None):
        return self.data

    def importRandomData(self, functions = 4):
        for n in range (7):
            self.data = np.append(self.data, np.random.uniform(-1, 1, functions))
        self.data = np.reshape(self.data, (7, functions))
        self.funcs = functions
        self.weighAndSortByProbability()

    def importData(self, data):
        self.data = np.array(data)
        self.funcs = np.shape(self.data)[1]
        self.weighAndSortByProbability()

    def weighAndSortByProbability(self):
        t = 0
        for i in range(self.funcs):
            self.data[6, i] = abs(self.data[6, i])
            t = t + self.data[6, i]
        for i in range(self.funcs):
            self.data[6, i] = self.data[6, i] / t
        for i in range(self.funcs):
            for j in range(0, self.funcs - i - 1):
                if (self.data[6, j] < self.data[6, j + 1]):
                    self.data[:, [j, j + 1]] = self.data[:, [j + 1, j]]

    def iterateLinear(self, reps = 100000):

        self.coords = np.empty([2, reps + 1])
        self.coords[0, 0] = 0
        self.coords[1, 0] = 0

        for n in range(reps):
            r = np.random.choice(np.arange(self.funcs), 1, p = self.data[6, :])
            self.coords[0, n + 1] = self.data[0, r] * self.coords[0, n] + self.data[1, r] * self.coords[1, n] + self.data[4, r]
            self.coords[1, n + 1] = self.data[2, r] * self.coords[0, n] + self.data[3, r] * self.coords[1, n] + self.data[5, r]

        self.coords = np.delete(self.coords, 0, 1)

    def iterateTrig(self, reps = 100000):

        self.coords = np.empty([2, reps + 1])
        self.coords[0, 0] = 0
        self.coords[1, 0] = 0

        for n in range(reps):
            r = np.random.choice(np.arange(self.funcs), 1, p = self.data[6, :])
            self.coords[0, n + 1] = self.data[0, r] * math.cos(self.data[2, r]) * self.coords[0, n] - self.data[1, r] * math.sin(self.data[3, r]) * self.coords[1, n] + self.data[4, r]
            self.coords[1, n + 1] = self.data[0, r] * math.sin(self.data[2, r]) * self.coords[0, n] + self.data[1, r] * math.cos(self.data[3, r]) * self.coords[1, n] + self.data[5, r]

        self.coords = np.delete(self.coords, 0, 1)

    def plot(self, windowWidth = 1000, windowHeight = 1000, fillWidth = 0.9, fillHeight = 0.9):
        img = Image.new(mode = "RGBA", size = (windowWidth, windowHeight), color = "WHITE")

        scaleX = (windowWidth / 2) / max(np.amax(self.coords[0]), abs(np.amin(self.coords[0])))
        scaleY = (windowHeight / 2) / max(np.amax(self.coords[1]), abs(np.amin(self.coords[1])))
        scaleX = scaleX * fillWidth
        scaleY = scaleY * fillHeight

        for n in range(np.shape(self.coords)[1]):
            img.putpixel((int(windowWidth / 2 + (self.coords[0, n] * scaleX)),
                          int(windowHeight / 2 - (self.coords[1, n] * scaleY))),
                          (0, 0, 0))

        img.show()

#a = ifs()
#a.importRandomData()
#a.iterateTrig()
#a.plot()
