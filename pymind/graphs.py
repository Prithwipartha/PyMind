from mind.dtypes import *
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d
import matplotlib.style as stl


class Point(Vector):
    def __init__(self, data):
        Vector.__init__(self, data)

    def dims(self):
        return len(self)


class Line:
    def __init__(self, points=[]):
        self.points = []
        self.dims = 0
        for point in points:
            self.add_point(point)

    def add_point(self, point=[]):
        if self.points is []:
            self.dims = len(point)
        self.points += [Point(point)]

    def dims(self):
        return self.dims


class LineSegment(Line):
    def __init__(self, start=None, stop=None):
        Line.__init__(self, [start, stop])


class SolidPlot:
    def __init__(self):
        self.points = []
        self.lines = []

    def new_point(self, point=[]):
        point = Point(point)
        if point.dims() is 3:
            self.points += [point]

    def new_line(self, points=[]):
        self.lines += [Line(points)]

    def new_cube(self, root=[], side=0):
        edges = []
        for i in [root[0], root[0] + side]:
            for j in [root[1], root[1] + side]:
                for k in [root[2], root[2] + side]:
                    edges += [[i, j, k]]
        for i in range(len(edges)):
            for j in range(i):
                a = 0
                for k in range(3):
                    if edges[i][k] is edges[j][k]:
                        a = a+1
                if a is 2:
                    self.new_line([edges[i], edges[j]])

        pass

    def plot(self, style='classic', line_type='-', line_col='k', line_width=1):
        stl.use(style)
        grid = plt.axes(projection='3d')
        grid.set_xlabel('<-- x -->')
        grid.set_ylabel('<-- y -->')
        grid.set_zlabel('<-- z -->')

        for i in self.points:
            grid.scatter(i[0], i[1], i[2])
        for i in self.lines:
            i = transpose(i.points)
            grid.plot(i[0], i[1], i[2], line_type+line_col, linewidth=line_width)
        plt.show()


class WavePlot:
    dims = 2
    sources = []

    def __init__(self, kind='2D'):
        if kind is not '2D':
            self.dims = 3

    def add_source(self, source=[], wavelength=1):
        self.sources += [[source, wavelength/6]]

    def show(self, till_mu=20):
        stl.use('dark_background')
        ax = plt.subplot()
        for i in range(till_mu*6):
            for j in self.sources:
                col = 'm'
                a = i % 6
                if a is 0:
                    col = 'r'
                elif a is 1:
                    col = 'y'
                elif a is 2:
                    col = 'g'
                elif a is 3:
                    col = 'c'
                elif a is 4:
                    col = 'b'
                elif col is 5:
                    col = 'm'
                ax.add_patch(plt.Circle(j[0], j[1]*i, color=col, fill=False, linewidth=1))
        stl.use('dark_background')
        plt.show()
