import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry
import random

espace = pc.EspaceDeTravail([(-20,-32), (-20,20), (0,25), (30,20), (30,-32), (-20,-32)])
listAngle = [0, m.pi/2, -m.pi/2]

def autoRoute(epaisseur, parking, nbRoutes):
    listAvailable = [(0, i) for i in range(3)]

    return autoRouteAux(epaisseur, parking, listAvailable, nbRoutes)

def autoRouteAux(epaisseur, parking, listAvailable, nbRoutes):
    #listAvailable de la forme [(0, 0), (0, 1)]
    if nbRoutes < 1:
        return parking
    longueur = len(listAvailable)
    index = random.randint(0, longueur - 1)
    route, angle = listAvailable[index]
    print(nbRoutes)
    route = parking[route]
    angle = listAngle[angle]
    a = pc.Route(route, random.random() * 20 + 5, epaisseur, angle, espace)
    if a.valide :
        parking += [a]
        nbRoutes -= 1
        listAvailable.pop(index)
        listAvailable += [(len(parking) - 1, i) for i in range(3)]
        return autoRouteAux(epaisseur, parking, listAvailable, nbRoutes)
    return autoRouteAux(epaisseur, parking, listAvailable, nbRoutes)



parking = [pc.Rampe(20, 5, [-25,0], 0, 2)]
#parking += [pc.Noyaux(parking, [(10,10), (10,15), (20,15), (20,10), (10,10)])]
parking = autoRoute(5, parking, 10)


parking = pc.remplissagePlace(parking, 5, 2.5, espace)


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