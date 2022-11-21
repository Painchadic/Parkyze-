import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry

espace = pc.EspaceDeTravail([(-20,-32), (-20,20), (30,20), (30,-32), (-20,-32)])
parking = [pc.Rampe(20, 2, [-25,0], 0, 2)]
parking += [pc.Route(parking[0], 12, 2, 0)]
parking += [pc.Route(parking[1], 12, 2, 0)]
for i in range(3):
    parking += [pc.Route(parking[i], 31, 2, -parking[i].angle - m.pi/2)]

parking += [pc.Noyaux(parking, [(10,10), (10,15), (20,15), (20,10), (10,10)])]
parking += pc.remplissagePlace(parking, 5, 2.5)



poly = []

for i in parking:
    resX = []
    resY = []

    couleur, points = i.color, i.forme
    if (type(i) != pc.Rampe) :
        if (pc.gene(i, parking, 0.01)[0]) or not(pc.inEspaceDeTravail(points, espace.forme)):
            continue

    poly += [points]
    resX, resY = points.exterior.xy
    if type(i) == pc.Route :
        py.fill(resX,resY, color = 'k')
    py.plot(resX,resY, color = couleur)

resX, resY = espace.forme.exterior.xy
py.plot(resX,resY, color = espace.color)

a,b,c,d = pc.camera(espace)
py.xlim(a,b)
py.ylim(c,d)
py.show()

print(parking[-1].distanceRoute)
print(parking[-1].pere)
print(parking[0].fils)