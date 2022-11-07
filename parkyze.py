from turtle import color
import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry

parking = [pc.Rampe(5, 2, [0,0], 0, 2)]
parking += [pc.Route(parking[0], 12, 2, m.pi/2)]
for i in range(2):
    parking += [pc.Route(parking[i], 16, 2, -parking[i].angle + m.pi/4)]
    yay = parking[-1]
    for j in np.arange(2.25,15.75,2.5):
        parking += [pc.Place(yay, 5, 2.5, j, m.pi/2)]
        parking += [pc.Place(yay, 5, 2.5, j, -m.pi/2)]

parking += [pc.Noyaux(parking, [(10,10), (10,15), (20,15), (20,10), (10,10)])]

poly = []

for i in parking:
    resX = []
    resY = []
    couleur, points = i.color, i.forme
    if pc.gene(i, parking, 0.01) :
        continue
    poly += [points]
    resX, resY = points.exterior.xy
    if type(i) == pc.Route :
        py.fill(resX,resY, color = 'k')
    py.plot(resX,resY, color = couleur)
py.show()

print(parking[-1].distanceRoute)
print(parking[-1].pere)