
import matplotlib
matplotlib.use('Qt5Agg')

from datetime import datetime  # , date, time, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from numpy import sqrt, radians, sin, cos, pi
import csv


class Star:
    def __init__(self, object_name, color, m):
        self.M = m  # масса
        self.x = 0
        self.y = 0
        self.z = 0
        ax.scatter(self.x, self.y, self.z, c=color, s=50, edgecolors='black', lw=0.25)
        ax.text(self.x, self.y, self.z, object_name, fontsize=7.5)


class Object(object):
    def __init__(self, object_name, color, m, a, e, i, w, O, M, JD=2451545.0):
        """
        :param str object_name: название
        :param str color: цвет точки
        :param m: масса
        :param a: большая полуось КМ
        :param e: ексцентриситет ε e=c/a
        :param i: отклонение°
        :param w: аргумент перицентра° ω
        :param O: долгота восходящего узла° Ω N
        :param M: средняя аномалия° M=E-e*np.sin(E)
        :param JD: юлианская дата 2451545.0
        ∂ φ
        """
        self.name = object_name
        self.color = color
        self.m = m
        X, Y, Z = [], [], []
        p = a * (1 - e ** 2)  # фокальный параметр
        b = sqrt(a * p)  # малая полуось
        k = G * (SUN.M + self.m)  # µ гравитационный параметр
        n = sqrt(k / a ** 3)  # среднее движение
        T = 2 * pi / n  # период обращения sqrt(((4 * pi**2)/(G * (SUN.M + m))) * a**3)Кеплер 3
        E = radians(M)
        for count in range(int(999/365*(datetime.now() - get_g_d(JD)).days)):  # int(999/365*(datetime.now() - get_g_d(JD)).days)
            while abs((M + e * sin(E)) - E) > 0.00001:  # последовательные приближения для эксцентрической аномалии
                E = M + e * sin(E)
            M += n * 1  # M = n(t−t0)+M0
            r = a * (1 - e * cos(E))  # радиус-вектор
            sinv = (sqrt(1 - e ** 2) * sin(E)) / (1 - e * cos(E))
            cosv = (cos(E) - e) / (1 - e * cos(E))
            sinu = sin(radians(w)) * cosv + cos(radians(w)) * sinv
            cosu = cos(radians(w)) * cosv - sin(radians(w)) * sinv
            X.append(r * (cosu * cos(radians(O)) - sinu * sin(radians(O)) * cos(radians(i))))
            Y.append(r * (cosu * sin(radians(O)) + sinu * cos(radians(O)) * cos(radians(i))))
            Z.append(r * (sinu * sin(radians(i))))
            # V1 = sqrt(r / p) * e * sinv
            # V2 = sqrt(r / p) * (1 + e * cosv)
        # F = G * SUN.M * self.m / r ** 2  # сила гравитационного притяжения
        self.X = X
        self.Y = Y
        self.Z = Z
        # φ = (24 * pi**3 * a**2) / (T**2 * C**2 * (1 - e**2))
        # φ = (6 * pi * G * SUN.M) / (C**2 * a * (1 - e**2))
        # Rper = (1 - e) * a  # радиус перегелия
        # Rafe = (1 + e) * a  # радиус афелия

    def star(self):
        pass

    def planet(self, orbit=True):
        return self.paint(orbit=orbit, size_o=0.5)

    def satellite(self, major):
        pass

    def asteroid(self, orbit=False):
        return self.paint(orbit=orbit, size_o=0.25)

    def paint(self, orbit=True, size_o=0.5):
        pos = ax.scatter(self.X[-1], self.Y[-1], self.Z[-1], c=self.color, s=s_s(self.m), edgecolors='black', lw=0.25)
        txt = ax.text(self.X[-1], self.Y[-1], self.Z[-1], self.name, fontsize=7.5)
        orb = ax.plot(self.X, self.Y, self.Z, '-', c='black', lw=size_o) if orbit else None
        way = ax.plot([self.X[-1], self.X[-1]], [self.Y[-1], self.Y[-1]], [self.Z[-1], 0], '--', c='black', lw=0.25)
        return pos, txt, orb, way


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


def s_s(m):
    if m > 1e25:
        return 10
    elif m > 1e23:
        return 5
    elif m > 1e20:
        return 2.5
    elif m > 1e18:
        return 0.25
    else:
        return 0.1


if __name__ == '__main__':
    G = 6.67408e-11  # граивтационная постоянная м3·с−2·кг−1 или Н·м2·кг−2
    au = 149597870  # а.е. астрономическая единица
    C = 299792458  # скорость света м/с

    # настройки окна
    fig = plt.figure(figsize=(8, 8))  # , dpi=100  , frameon=False , edgecolor='k'
    fig.canvas.set_window_title('Planet system beta ver')
    plt.subplots_adjust(bottom=0, right=1, left=0, top=1)
    ax = plt.gca(projection='3d')
    ax.set_title('Planet system')
    ax.axis('off')  # оси координат
    ax.grid(True)  # сетка
    ax.set_xlabel('X')  # подпись осей
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # цвет панелей
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))  # цвет сетки
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.set_xlim([-2e10, 2e10])
    ax.set_ylim([-2e10, 2e10])
    ax.set_zlim([-2e10, 2e10])

    SUN = Star('Sun', 'yellow', m=1.98892e30)  # J2000.0 JD2451545.0

    MERCURY = Object('Mercury', 'gray', m=3.33022e23, a=57909227, e=0.20563593, i=7.00487, w=29.124279,
                     O=48.33167, M=174.795884, JD=2451545.0).planet()
    VENUS = Object('Venus', 'brown', m=4.8675e24, a=108209475, e=0.00677323, i=3.39471, w=54.85229, O=76.67069,
                   M=50.115, JD=2451545.0).planet()
    EARTH = Object('Earth', 'blue', m=5.9726e24, a=149598262, e=0.01671022, i=0.00005, w=114.20783, O=348.73936,
                   M=358.617, JD=2451545.0).planet()
    MARS = Object('Mars', 'red', m=6.4185e23, a=227943824, e=0.09341233, i=1.85061, w=286.46230, O=49.57854,
                  M=19.373, JD=2451545.0).planet()
    JUPITER = Object('Jupiter', 'gold', m=1.8986e27, a=778340821, e=0.04839266, i=1.30530, w=275.066, O=100.55615,
                     M=20.020, JD=2451545.0).planet()
    SATURN = Object('Saturn', 'yellow', m=5.6846e26, a=1433449370, e=0.055723219, i=2.485240, w=336.013862, O=113.71504,
                    M=317.020, JD=2451545.0).planet()
    URANUS = Object('Uranus', 'green', m=8.6832e25, a=2870658186, e=0.04716771, i=0.76986, w=96.541318, O=74.22988,
                    M=142.238600, JD=2451545.0).planet()
    NEPTUNE = Object('Neptune', 'blue', m=1.0243e26, a=4498396441, e=0.00858587, i=1.76917, w=265.646853, O=131.72169,
                     M=256.228, JD=2451545.0).planet()

    CARES = Object('Ceres', 'gray', m=9.393e20, a=413767000, e=0.07934, i=10.585, w=2.825, O=80.399, M=27.448,
                   JD=2455000.5).planet()
    PLUTO = Object('Pluto', 'brown', m=1.303e22, a=5906440628, e=0.24880766, i=17.14175, w=113.76329, O=110.30347,
                   M=14.53, JD=2451545.0).planet()
    HAUMEA = Object('Haumea', 'gray', m=4.006e21, a=42.98492 * au, e=0.1975233, i=28.201975, w=240.582838, O=121.900456,
                    M=205.22317, JD=2456000.5).planet()
    MAKEMAKE = Object('Makemake', 'brown', m=3e21, a=45.436301 * au, e=0.16254481, i=29.011819, w=296.534594,
                      O=79.305348, M=153.854714, JD=2456000.5).planet()
    ERIS = Object('Eris', 'gray', m=1.66e22, a=67.781 * au, e=0.44068, i=44.0445, w=150.977, O=35.9531, M=204.16,
                  JD=2457000.5).planet()
    SEDNA = Object('Sedna', 'white', m=8.3e21, a=541.429506 * au, e=0.8590486, i=11.927945, w=310.920993, O=144.377238,
                   M=358.190921, JD=2456000.5).planet()

    with open('TNOs.csv') as csvfile:
        TNOs = csv.reader(csvfile)
        for row in TNOs:
            if row[6].isalpha():
                continue
            if row[0].split(' ')[-1].isalpha():
                name = row[0].split(' ')[-1]
            else:
                name = ''
            if name:
                date = get_j_d(int(row[5][6:8]), int(row[5][4:6]), int(row[5][0:4]))
                Object(name, 'gray', m=1e20, a=float(row[11]) * au, e=float(row[10]), i=float(row[9]),
                       w=float(row[7]), O=float(row[8]), M=float(row[6]), JD=date).asteroid()

    with open('Atens.csv') as csvfile:
        TNOs = csv.reader(csvfile)
        for row in TNOs:
            if row[7].isalpha():
                continue
            if row[0].split(' ')[-1].isalpha():
                name = row[0].split(' ')[-1]
            else:
                name = ''
            if name:
                date = get_j_d(int(row[6][6:8]), int(row[6][4:6]), int(row[6][0:4]))
                Object(name, 'gray', m=1e15, a=float(row[12]) * au, e=float(row[11]), i=float(row[10]),
                       w=float(row[8]), O=float(row[9]), M=float(row[7]), JD=date).asteroid()

    x, y, j = axes3d.get_test_data(0.05)  # ось эклиптики
    ECLIPTIC_p = ax.plot_wireframe(x * 500000000, y * 500000000, j * 0, rstride=15, cstride=15, alpha=0.25, lw=0.5)
    ECLIPTIC_t = ax.text(-15000000000, -15000000000, 0, 'Ecliptic', color='b', alpha=0.25)
    ARIES_p = ax.plot([0, 2e10], [0, 0], [0, 0], c='r', lw=0.5, alpha=0.5)  # точка овна
    ARIES_t = ax.text(2e10, 0, 0, 'Aries', color='r', alpha=0.5)

    plt.show()

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
