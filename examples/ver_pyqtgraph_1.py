#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from numpy import sqrt, radians, sin, cos, pi, vstack, array
import csv

from stellarpy import Star, Body


au = 149597870.700  # а.е. астрономическая единица

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
MERCURY = Body('Mercury', color=(.5, .5, .5, 1), major=SUN, m=3.33022e23, at=0.0005861,
               a=57909227, e=0.20563593, i=7.00487, w=29.124279, O=48.33167, M=174.795884)
VENUS = Body('Venus', color=(0.3, 0, 0, 1), major=SUN, m=4.8675e24, at=177.36,
             a=108209475, e=0.00677323, i=3.39471, w=54.85229, O=76.67069, M=50.115)
EARTH = Body('Earth', color=(0, 0, 1, 1), major=SUN, m=5.9726e24, at=23.439,
             a=149598262, e=0.01671022, i=0.00005, w=114.20783, O=348.73936, M=358.617)
MARS = Body('Mars', color=(1, 0, 0, 1), major=SUN, m=6.4185e23, at=25.1919,
            a=227943824, e=0.09341233, i=1.85061, w=286.46230, O=49.57854, M=19.373)
JUPITER = Body('Jupiter', color=(.5, .5, 0, 1), major=SUN, m=1.8986e27, at=3.13,
               a=778340821, e=0.04839266, i=1.30530, w=275.066, O=100.55615, M=20.020)
SATURN = Body('Saturn', color=(1, 1, 0, 1), major=SUN, m=5.6846e26, at=26.73,
              a=1433449370, e=0.055723219, i=2.485240, w=336.013862, O=113.71504, M=317.020)
URANUS = Body('Uranus', color=(0, 0.5, 0, 1), major=SUN, m=8.6832e25, at=97.77,
              a=2870658186, e=0.04716771, i=0.76986, w=96.541318, O=74.22988, M=142.238600)
NEPTUNE = Body('Neptune', color=(0, 0, .5, 1), major=SUN, m=1.0243e26, at=28.32,
               a=4498396441, e=0.00858587, i=1.76917, w=265.646853, O=131.72169, M=256.228)
CARES = Body('Ceres', color=(.5, .5, .5, 1), major=SUN, m=9.393e20, at=3,
             a=413767000, e=0.07934, i=10.585, w=2.825, O=80.399, M=27.448,
             JD=2455000.5)
PLUTO = Body('Pluto', color=(0.3, 0, 0, 1), major=SUN, m=1.303e22, at=119.591,
             a=5906440628, e=0.24880766, i=17.14175, w=113.76329, O=110.30347, M=14.53,
             JD=2451545.0)
HAUMEA = Body('Haumea', color=(.5, .5, .5, 1), major=SUN, m=4.006e21, at=0,
              a=42.98492 * au, e=0.1975233, i=28.201975, w=240.582838, O=121.900456, M=205.22317,
              JD=2456000.5)
MAKEMAKE = Body('Makemake', color=(0.3, 0, 0, 1), major=SUN, m=3e21, at=0,
                a=45.436301 * au, e=0.16254481, i=29.011819, w=296.534594, O=79.305348, M=153.854714,
                JD=2456000.5)
ERIS = Body('Eris', color=(.5, .5, .5, 1), major=SUN, m=1.66e22, at=0,
            a=67.781 * au, e=0.44068, i=44.0445, w=150.977, O=35.9531, M=204.16,
            JD=2457000.5)
SEDNA = Body('Sedna', color=(.5, .5, .5, 1), major=SUN, m=8.3e21, at=0,
             a=541.429506 * au, e=0.8590486, i=11.927945, w=310.920993, O=144.377238, M=358.190921,
             JD=2456000.5)

BODIES = [MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, CARES, PLUTO, HAUMEA, MAKEMAKE, ERIS, SEDNA]

try:
    with open('SBD.csv') as csvfile:
        objects = csv.reader(csvfile)
        next(objects)
        for row in objects:
            if row[7]:
                try:
                    BODIES.append(Body(row[7], major=SUN, m=1e20, a=float(row[0]) * au, e=float(row[1]), 
                                       i=float(row[2]), w=float(row[3]), O=float(row[4]), M=float(row[5]), 
                                       JD=float(row[6])))
                except ValueError:
                    continue
except FileNotFoundError:
    pass

for j in range(len(BODIES)):
    combo.addItem(BODIES[j].name)


class Paint:
    def __init__(self, body):
        """
        :param class body: объект
        """
        self.color = body.color
        self.orbit = body.orbit
        self.guide = body.guide
        self.size = body.size
        self.width = body.width
        self.X = body.X
        self.Y = body.Y
        self.Z = body.Z
        self.pos = gl.GLScatterPlotItem(pos=array([self.X[-1], self.Y[-1], self.Z[-1]]), size=self.size, color=self.color)
        self.pos.setGLOptions('translucent')
        plot_wid.addItem(self.pos)
        pts_way = vstack([(self.X[-1], self.X[-1]), (self.Y[-1], self.Y[-1]), (self.Z[-1], 0)]).transpose()
        self.way = gl.GLLinePlotItem(pos=pts_way, width=0.1, color=(0, 0, 0, .5), antialias=True)
        plot_wid.addItem(self.way) if self.guide else None
        pts_orb = vstack([self.X, self.Y, self.Z]).transpose()
        self.orb = gl.GLLinePlotItem(pos=pts_orb, width=self.width, color=(0, 0, 0, 1), antialias=True)
        plot_wid.addItem(self.orb) if self.orbit else None


BODIES_PAINT = []
for j in range(len(BODIES)):
    BODIES_PAINT.append(Paint(BODIES[j]))

# анимация
j = 0


def move():
    global j
    for l in range(len(BODIES_PAINT)):
        if len(BODIES_PAINT[l].X) > j:
            BODIES_PAINT[l].pos.setData(pos=array([BODIES_PAINT[l].X[j], BODIES_PAINT[l].Y[j], BODIES_PAINT[l].Z[j]]))
            pts_way = vstack([(BODIES_PAINT[l].X[j], BODIES_PAINT[l].X[j]),
                              (BODIES_PAINT[l].Y[j], BODIES_PAINT[l].Y[j]),
                              (BODIES_PAINT[l].Z[j], 0)]).transpose()
            BODIES_PAINT[l].way.setData(pos=pts_way, antialias=True)
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
