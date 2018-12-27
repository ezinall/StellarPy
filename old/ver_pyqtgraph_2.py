#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from numpy import sqrt, radians, sin, cos, pi, vstack, array
import csv


class Star:
    def __init__(self, object_name, m, color=(1, 1, 0, 1)):
        self.name = object_name
        self.M = m  # масса
        self.x = 0
        self.y = 0
        self.z = 0
        pos = gl.GLScatterPlotItem(pos=array([0, 0, 0]), color=color, size=10)
        pos.setGLOptions('translucent')
        plot_wid.addItem(pos)


class Object:
    def __init__(self, object_name, m, a, e, i, w, O=0, M=0, at=0, JD=2451545.0, color=(.5, .5, .5, 1)):
        """
        :param str object_name: название
        :param tuple color: цвет точки
        :param JD: юлианская дата 2451545.0
        :param float m: масса
        :param float at: наклон оси
        :param float a: большая полуось КМ
        :param float e: ексцентриситет ε e=c/a
        :param float i: отклонение°
        :param float w: аргумент перицентра° ω
        :param float O: долгота восходящего узла° Ω N
        :param float M: средняя аномалия° M=E-e*sin(E)
        ∂ φ
        """
        self.name = object_name
        self.color = color
        self.m = m
        self.at = at
        self.JD = JD
        self.pos = None
        self.orb = None
        self.way = None
        k = G * (SUN.M + m)  # µ гравитационный параметр
        n = sqrt(k / a ** 3)  # среднее движение
        self.T = 2 * pi / n  # период обращения sqrt(((4 * pi**2)/(G * (SUN.M + m))) * a**3) Кеплер 3
        x, y, z = [], [], []
        E = radians(M)
        self.age = int(999 / 365 * (datetime.now() - get_g_d(JD)).days)
        for count in range(self.age):
            while abs((M + e * sin(E)) - E) > 0.00001:  # последовательные приближения для эксцентрической аномалии
                E = M + e * sin(E)
            M += n * 1  # M = n(t−t0)+M0
            r = a * (1 - e * cos(E))  # радиус-вектор
            sin_v = (sqrt(1 - e ** 2) * sin(E)) / (1 - e * cos(E))
            cos_v = (cos(E) - e) / (1 - e * cos(E))
            sin_u = sin(radians(w)) * cos_v + cos(radians(w)) * sin_v
            cos_u = cos(radians(w)) * cos_v - sin(radians(w)) * sin_v
            x.append(r * (cos_u * cos(radians(O)) - sin_u * sin(radians(O)) * cos(radians(i))))
            y.append(r * (cos_u * sin(radians(O)) + sin_u * cos(radians(O)) * cos(radians(i))))
            z.append(r * (sin_u * sin(radians(i))))
            # V1 = sqrt(r / p) * e * sinv
            # V2 = sqrt(r / p) * (1 + e * cosv)
        self.X = list(reversed(x)) if self.at > 90 else x
        self.Y = list(reversed(y)) if self.at > 90 else y
        self.Z = list(reversed(z)) if self.at > 90 else z
        # self.X = x
        # self.Y = y
        # self.Z = z
        # F = G * SUN.M * self.m / r ** 2  # сила гравитационного притяжения
        # p = a * (1 - e ** 2)  # фокальный параметр
        # b = sqrt(a * p)  # малая полуось
        # Rper = (1 - e) * a  # радиус перегелия
        # Rafe = (1 + e) * a  # радиус афелия
        # φ = (24 * pi**3 * a**2) / (T**2 * C**2 * (1 - e**2))
        # φ = (6 * pi * G * SUN.M) / (C**2 * a * (1 - e**2))

        if self.m > 1e25:
            self.outer_planets()
        elif self.m > 1e23:
            self.planet()
        elif self.m > 1e20:
            self.dwarf_planet()
        else:
            self.small_body()

    def star(self):
        pass

    def planet(self, orbit=True, way=True, size=8, width=1):
        return self.paint(orbit=orbit, way=way, size=size, width=width)

    def outer_planets(self, orbit=True, way=True, size=10, width=1):
        return self.paint(orbit=orbit, way=way, size=size, width=width)

    def dwarf_planet(self, orbit=True, way=True, size=6, width=1):
        return self.paint(orbit=orbit, way=way, size=size, width=width)

    def small_body(self, orbit=False, way=False, size=1.5, width=.25):
        return self.paint(orbit=orbit, way=way, size=size, width=width)

    def satellite(self, major, orbit=False, way=False, size=4, width=1):
        pass

    def paint(self, orbit=True, way=True, size=4.0, width=1.0):
        self.pos = gl.GLScatterPlotItem(pos=array([self.X[-1], self.Y[-1], self.Z[-1]]), size=size, color=self.color)
        self.pos.setGLOptions('translucent')
        plot_wid.addItem(self.pos)
        pts_way = vstack([(self.X[-1], self.X[-1]), (self.Y[-1], self.Y[-1]), (self.Z[-1], 0)]).transpose()
        self.way = gl.GLLinePlotItem(pos=pts_way, width=0.1, color=(0, 0, 0, .5), antialias=True)
        plot_wid.addItem(self.way) if way else None
        pts_orb = vstack([self.X, self.Y, self.Z]).transpose()
        self.orb = gl.GLLinePlotItem(pos=pts_orb, width=width, color=(0, 0, 0, 1), antialias=True)
        plot_wid.addItem(self.orb) if orbit else None


def get_g_d(j_d):
    a = int(j_d + 32044)
    b = int((4 * a + 3) / 146097)
    c = a - int((146097 * b) / 4)
    d = int((4 * c + 3) / 1461)
    e = c - int((1461 * d) / 4)
    m = int((5 * e + 2) / 153)
    day = e - int((153 * m + 2) / 5) + 1
    month = m + 3 - 12 * int((m / 10))
    year = 100 * b + d - 4800 + int((m / 10))
    return datetime(year, month, day)


def get_j_d(day, month, year):
    a = int((14 - month) / 12)
    b = year + 4800 - a
    c = month + 12 * a - 3
    return day + int((153 * c + 2) / 5) + 365 * b + int(b / 4) - int(b / 100) + int(b / 400) - 32045


G = 6.67408e-11  # граивтационная постоянная м3·с−2·кг−1 или Н·м2·кг−2
AU = 149597870.700  # а.е. астрономическая единица
C = 299792458  # скорость света м/с

# настройки окна
app = QtGui.QApplication([])

win = QtGui.QWidget()
win.setWindowTitle('Planet System beta')
win.setGeometry(200, 50, 1024, 768)
win.show()

layout = QtGui.QGridLayout()
layout.setColumnStretch(0, 1)
layout.setColumnMinimumWidth(1, 100)
win.setLayout(layout)

plot_wid = gl.GLViewWidget()
plot_wid.setBackgroundColor('w')
plot_wid.opts['distance'] = 50000000000
plot_wid.orbit(-90, 10)

combo = QtGui.QComboBox()
combo.addItem('Все')
check_o = QtGui.QCheckBox(text='Орбита')
check_O = QtGui.QCheckBox(text='Долгота')

layout.addWidget(plot_wid, 0, 0, 10, 1)
layout.addWidget(combo, 0, 1, 1, 2)
layout.addWidget(check_o, 1, 1)
layout.addWidget(check_O, 1, 2)

# ось эклиптики (сетка)
g = gl.GLGridItem(color=[0, 0, 1, .1])
g.setSize(x=50000000000, y=50000000000)
g.setSpacing(x=700000000, y=700000000)
plot_wid.addItem(g)

# точка овна
pts_ARIES = vstack([(0, 2e10), (0, 0), (0, 0)]).transpose()
ARIES_p = gl.GLLinePlotItem(pos=pts_ARIES, width=0.1, color=(1, 0, 0, 1), antialias=True)
plot_wid.addItem(ARIES_p)
# ARIES_t = ax.text(2e10, 0, 0, 'Aries', color='r', alpha=0.5)

SUN = Star('Sun', m=1.98892e30)  # J2000.0 JD2451545.0
MERCURY = Object('Mercury', color=(.5, .5, .5, 1), m=3.33022e23, at=0.0005861,
                 a=57909227, e=0.20563593, i=7.00487, w=29.124279, O=48.33167, M=174.795884)
VENUS = Object('Venus', color=(0.3, 0, 0, 1), m=4.8675e24, at=177.36,
               a=108209475, e=0.00677323, i=3.39471, w=54.85229, O=76.67069, M=50.115)
EARTH = Object('Earth', color=(0, 0, 1, 1), m=5.9726e24, at=23.439,
               a=149598262, e=0.01671022, i=0.00005, w=114.20783, O=348.73936, M=358.617)
MARS = Object('Mars', color=(1, 0, 0, 1), m=6.4185e23, at=25.1919,
              a=227943824, e=0.09341233, i=1.85061, w=286.46230, O=49.57854, M=19.373)
JUPITER = Object('Jupiter', color=(.5, .5, 0, 1), m=1.8986e27, at=3.13,
                 a=778340821, e=0.04839266, i=1.30530, w=275.066, O=100.55615, M=20.020)
SATURN = Object('Saturn', color=(1, 1, 0, 1), m=5.6846e26, at=26.73,
                a=1433449370, e=0.055723219, i=2.485240, w=336.013862, O=113.71504, M=317.020)
URANUS = Object('Uranus', color=(0, 0.5, 0, 1), m=8.6832e25, at=97.77,
                a=2870658186, e=0.04716771, i=0.76986, w=96.541318, O=74.22988, M=142.238600)
NEPTUNE = Object('Neptune', color=(0, 0, .5, 1), m=1.0243e26, at=28.32,
                 a=4498396441, e=0.00858587, i=1.76917, w=265.646853, O=131.72169, M=256.228)
CARES = Object('Ceres', color=(.5, .5, .5, 1), m=9.393e20, at=3,
               a=413767000, e=0.07934, i=10.585, w=2.825, O=80.399, M=27.448,
               JD=2455000.5)
PLUTO = Object('Pluto', color=(0.3, 0, 0, 1), m=1.303e22, at=119.591,
               a=5906440628, e=0.24880766, i=17.14175, w=113.76329, O=110.30347, M=14.53,
               JD=2451545.0)
HAUMEA = Object('Haumea', color=(.5, .5, .5, 1), m=4.006e21, at=0,
                a=42.98492 * AU, e=0.1975233, i=28.201975, w=240.582838, O=121.900456, M=205.22317,
                JD=2456000.5)
MAKEMAKE = Object('Makemake', color=(0.3, 0, 0, 1), m=3e21, at=0,
                  a=45.436301 * AU, e=0.16254481, i=29.011819, w=296.534594, O=79.305348, M=153.854714,
                  JD=2456000.5)
ERIS = Object('Eris', color=(.5, .5, .5, 1), m=1.66e22, at=0,
              a=67.781 * AU, e=0.44068, i=44.0445, w=150.977, O=35.9531, M=204.16,
              JD=2457000.5)
SEDNA = Object('Sedna', color=(.5, .5, .5, 1), m=8.3e21, at=0,
               a=541.429506 * AU, e=0.8590486, i=11.927945, w=310.920993, O=144.377238, M=358.190921,
               JD=2456000.5)
GOBLIN = Object('Goblin', color=(.5, .5, .5, 1), m=1e22, at=0,
                a=1051.1553620972 * AU, e=0.938315969096, i=11.663860890828, w=118.31762541793, O=300.89644655575, M=359.4,
                JD=2458200.5)

BODIES = [MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, CARES, PLUTO, HAUMEA, MAKEMAKE, ERIS, SEDNA, GOBLIN]

try:
    with open('SBD.csv') as csvfile:
        objects = csv.reader(csvfile)
        next(objects)
        for row in objects:
            if row[7]:
                try:
                    BODIES.append(Object(row[7], m=1e20, a=float(row[0]) * AU, e=float(row[1]), i=float(row[2]),
                                         w=float(row[3]), O=float(row[4]), M=float(row[5]), JD=float(row[6])))
                except ValueError:
                    continue
except FileNotFoundError:
    pass

for j in range(len(BODIES)):
    combo.addItem(BODIES[j].name)

# анимация
j = 0


def move():
    global j
    for l in range(len(BODIES)):
        if len(BODIES[l].X) > j:
            BODIES[l].pos.setData(pos=array([BODIES[l].X[j], BODIES[l].Y[j], BODIES[l].Z[j]]))
            pts_way = vstack([(BODIES[l].X[j], BODIES[l].X[j]),
                              (BODIES[l].Y[j], BODIES[l].Y[j]),
                              (BODIES[l].Z[j], 0)]).transpose()
            BODIES[l].way.setData(pos=pts_way, antialias=True)
    j += 1
    timer.timeout.disconnect(move) if j >= len(MERCURY.X) else None


timer = QtCore.QTimer()
timer.timeout.connect(move)
timer.start(10)

if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    # sys.exit(app.exec_())

# import pyqtgraph.examples
# pyqtgraph.examples.run()


'''
        T = str(round(T/1000, 2)) + ' yers' if T/1000 > 1 else str(round(365/100 * T/10, 2)) + ' days'

        from numpy import sqrt, radians, sin, cos, arctan2
        #E = M + e * sin(radians(M)) * (1 + e * cos(radians(M)))  # эксцентрическая аномалия
        E = radians(M)
        while abs((M + e * sin(E)) - E) > 0.00001:  # метод последовательных приближений для эксцентрической аномалии
            E = M + e * sin(E)
        xv = a * (cos(E) - e)  # ξ
        yv = a * (sqrt(1 - e ** 2) * sin(E))  # η
        zv = 0  # ζ
        r = sqrt(xv ** 2 + yv ** 2 + zv ** 2)  # радиус-вектор r=a*(1-e*np.cos(E))  xv*xv+yv*yv+zv*zv
        v = arctan2(yv, xv)  # истинная аномалия ν
        u = radians(w) + v  # аргумент широты
        xh = r * (cos(radians(O)) * cos(u) - sin(radians(O)) * sin(u) * cos(radians(i)))
        yh = r * (sin(radians(O)) * cos(u) + cos(radians(O)) * sin(u) * cos(radians(i)))
        zh = r * (sin(u) * sin(radians(i)))
        ax.scatter(xh, yh, zh, c=color, s=size_scatter(m), edgecolors='black', linewidth=0.25)
        ax.text(xh, yh, zh, name, fontsize=7.5)
'''