import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry
import random
import signal
import time

espace = pc.EspaceDeTravail([(-20,-32), (-20,20), (50,20), (50,-32), (-20,-32)])
rampe = pc.Rampe(15, 5, [-25,0], 0, 2)

def remplissageAutoParkingStandart1(espace, rampe, largeurRoute, longueurPlace, largeurPlace):
    parking = [rampe]

    longueurOpti = largeurRoute + 2*longueurPlace

    construire = True
    firstTurn = True
    angle = 0
    while construire:
        route = pc.Route(parking[-1], longueurOpti, largeurRoute, 0, espace)
        if route.valide :
            parking += [route]
            firstTurn = False
        elif firstTurn :
            if angle > m.pi :
                break
            angle += m.pi/2
        else :
            construire = False

    res = len(parking)

    for i in range(res):
        parking += [pc.maxRoad(parking[i], largeurRoute, m.pi/2, espace, 1)]
        parking += [pc.maxRoad(parking[i], largeurRoute, -m.pi/2, espace, 1)]

    return pc.remplissagePlace(parking, longueurPlace, largeurPlace, espace)

def remplissageAutoParkingStandart2(espace, rampe, largeurRoute, longueurPlace, largeurPlace):
    parking = [rampe]

    longueurOpti = largeurRoute + 2*longueurPlace

    parking += [pc.maxRoad(parking[0], largeurRoute, m.pi/2, espace, 1)]

    parking[1].cutEnd(longueurPlace)

    aba = parking[1].longueur
    a = aba%longueurOpti
    lng = a

    while lng < aba:
        parking += parking[-1].cut(lng)
        lng += longueurOpti
        
    construire = True

    route = pc.Route(parking[0], longueurOpti-a, largeurRoute, -m.pi/2 , espace)
    if route.valide :
        parking += [route]
    else :
        construire = False

    while construire:
        route = pc.Route(parking[-1], longueurOpti, largeurRoute, 0, espace)
        if route.valide :
            parking += [route]
        else :
            construire = False

    for i in range(1, len(parking)):
        parking += [pc.maxRoad(parking[i], largeurRoute, parking[0].angle - parking[i].angle , espace, 1)]

    return pc.remplissagePlace(parking, longueurPlace, largeurPlace, espace)


def remplissageAutoParkingStandart3(espace, rampe, largeurRoute, longueurPlace, largeurPlace):
    parking = [rampe]

    longueurOpti = largeurRoute + 2*longueurPlace

    parking += [pc.maxRoad(parking[0], largeurRoute, m.pi/2, espace, 1)]

    parking[1].cutEnd(longueurPlace)

    coinAireUn = []


    return pc.remplissagePlace(parking, longueurPlace, largeurPlace, espace)


parking = remplissageAutoParkingStandart3(espace, rampe, 5, 5, 2.5)

print(pc.distSortie(parking[0]))
print(pc.nbPlace(parking))
print(pc.ratio(parking,espace))
#for i in parking:
#    if type(i) == pc.Route :
#        print(i)


for i in parking:
    resX = []
    resY = []

    couleur, points = i.color, i.forme
    if (type(i) != pc.Rampe) :
        if (pc.gene(i, parking, 0.01)[0]):
            continue
    
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
