import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.animation as animation


def anim(j):
    Mercury.PLT._offsets3d = Mercury.CRD[j]
    Venus.PLT._offsets3d = Venus.CRD[j]
    Earth.PLT._offsets3d = Earth.CRD[j]
    Mars.PLT._offsets3d = Mars.CRD[j]
    Jupiter.PLT._offsets3d = Jupiter.CRD[j]
    Saturn.PLT._offsets3d = Saturn.CRD[j]
    Uranus.PLT._offsets3d = Uranus.CRD[j]
    Neptune.PLT._offsets3d = Neptune.CRD[j]
    Pluto.PLT._offsets3d = Pluto.CRD[j]


class Star:
    def __init__(self):
        Star.geometry(self)

    def geometry(self):
        STAR = ax.scatter(0, 0, c='yellow', s=50)


class Planet:
    def __init__(self, name, a, e, i, O, w, M0=0, v=0, E=0, color='b'):
        self.NAME = name
        self.COLOR = color
        self.a = a  # a- большая полуось КМ
        self.e = e  # e - ексцентриситет e=c/a
        self.M0 = M0  # M0 - cредняя аномалия°
        self.i = i  # i - отклонение°
        self.O = O  # O - долгота восходящего узла°
        self.w = w  # w - аргумент перицентра°
        self.v = v  # v - истинная аномалия°
        self.E = E  # E - эксцентрическая аномалия°
        self.u = self.v + self.w  # u - аргумент широты°
        self.CRD, self.PLT = Planet.orbit(self)

    def coordinates(self):
        RADi = np.radians(self.i)  # отклонения в радианах
        RADO = np.radians(self.O)  # долгота восходящего узла в радианах
        RADu = np.radians(self.u)  # аргумент широты в радианах
        r = self.a * (1 - self.e * np.cos(self.E))
        X = r * (np.cos(RADu) * np.cos(RADO) - np.sin(RADu) * np.sin(RADO) * np.cos(RADi))
        Y = r * (np.cos(RADu) * np.sin(RADO) - np.sin(RADu) * np.cos(RADO) * np.cos(RADi))
        Z = r * np.sin(RADu) * np.sin(RADi)

    def orbit(self):  # точка вес. равноденствия - X=0
        c = self.e * self.a  # половина фокусного расстояния КМ
        b = (self.a ** 2 - c ** 2) ** 0.5  # малая полуось КМ
        RADi = np.radians(self.i)  # отклонения в радианах
        RADO = np.radians(self.O)  # долгота восходящего узла в радианах
        RADw = np.radians(self.w)  # арг. перицентра° в радианах
        t = np.linspace(0, 2 * np.pi, 100)  # параметр (для эллепса)
        X = self.a * np.cos(t) - c
        Y = b * np.sin(t)
        Z = t * 0
        Xi = X * np.cos(RADi) + Z * np.sin(RADi)
        Zi = X * np.sin(RADi) + Z * np.cos(RADi)
        X = Xi;
        Z = Zi
        XO = X * np.cos(RADO) - Y * np.sin(RADO)
        YO = X * np.sin(RADO) + Y * np.cos(RADO)
        X = XO;
        Y = YO
        ################################################
        Yw = Y + (Y * np.cos(RADw) - Z * np.sin(RADw))
        Zw = Y + (Z * np.cos(RADw) + Z * np.sin(RADw))
        #Y=Yw; Z=Zw

        ORB = ax.plot(X, Y, Z, '-', c='black')
        PLT = ax.scatter(X[0], Y[0], Z[0], c=self.COLOR)
        CRD = np.zeros((100, 3, 1))
        for i in range(len(CRD)):
            CRD[i][0] = X[i]
            CRD[i][1] = Y[i]
            CRD[i][2] = Z[i]
        return CRD, PLT


fig = plt.figure(figsize=(10, 10), frameon=True)
ax = plt.gca(projection='3d')

au = 149597870700  # а.е. М
G = 6.67408 * (10 ** -11)  # гравитационная постоянна м^3 кг^-1 с^-2
c = 299792458  # скорость света в вакууме м*с^−1

Sun = Star()
Mercury = Planet(name='Mercury', color='gray',
                 a=57909227, e=0.20563069, M0=174.795884, i=7.00487, O=48.33167, w=29.124279)
Venus = Planet(name='Venus', color='brown',
               a=108209475, e=0.00677323, i=3.39471, O=76.67069, w=54.85229)
Earth = Planet(name='Earth', color='blue',
               a=149598262, e=0.01671022, i=0.00005, O=348.73936, w=114.20783)
Mars = Planet(name='Mars', color='red',
              a=227943824, e=0.09341233, i=1.85061, O=49.57854, w=286.46230)
Jupiter = Planet(name='Jupiter', color='gold',
                 a=778340821, e=0.04839266, i=1.30530, O=100.55615, w=275.066)
Saturn = Planet(name='Saturn', color='brown',
                a=1426666422, e=0.05415060, i=2.48446, O=113.71504, w=336.013862)
Uranus = Planet(name='Uranus', color='lightblue',
                a=2870658186, e=0.04716771, i=0.76986, O=74.22988, w=96.541318)
Neptune = Planet(name='Neptune', color='blue',
                 a=4498396441, e=0.00858587, i=1.76917, O=131.72169, w=265.646853)
Pluto = Planet(name='Pluto', color='brown',
               a=5906440628, e=0.24880766, i=17.14175, O=110.30347, w=113.76329)

X, Y, Z = axes3d.get_test_data(0.05)
ECLIPTICp = ax.plot_wireframe(X * 300000000, Y * 300000000, Z * 0, rstride=15, cstride=15, alpha=0.25, lw=0.5)
ECLIPTICt = ax.text(-8000000000, -8000000000, 0, 'Ecliptic', color='b', alpha=0.25)
ARIESp = ax.plot(np.linspace(0, 0, 100), np.linspace(0, -10000000000, 100), np.linspace(0, 0, 100), c='r', lw=0.5)
ARIESt = ax.text(0, -10250000000, 0, 'Aries', color='r')
ANIMATION = animation.FuncAnimation(fig, anim) #  fargs=(Mercury.PLT, Mercury.CRD)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.axis('off')
# i=8; j=3
i = 9
j = 7
ax.set_xlim([-j * 10 ** i, j * 10 ** i, ])
ax.set_ylim([-j * 10 ** i, j * 10 ** i, ])
ax.set_zlim([-j * 10 ** i, j * 10 ** i, ])
# plt.grid()
plt.show()
