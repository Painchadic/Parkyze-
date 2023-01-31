import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry
import random
import signal
import time

espace = pc.EspaceDeTravail([(-20,-32), (-20,20), (30,20), (30,-32), (-20,-32)])
rampe = pc.Rampe(16, 5, [0,-40], m.pi/2, 2)

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

    parking += [pc.maxRoad(parking[-1], largeurRoute, 0, espace, 0.1)]

    for i in range(1, len(parking) - 1):
        parking += [pc.maxRoad(parking[i], largeurRoute, parking[0].angle - parking[i].angle , espace, 1)]

    return pc.remplissagePlace(parking, longueurPlace, largeurPlace, espace)


def remplissageAutoParkingStandart3(espace, rampe, largeurRoute, longueurPlace, largeurPlace):
    parking = [rampe]

    longueurOpti = largeurRoute + 2*longueurPlace

    parking += [pc.maxRoad(parking[0], largeurRoute, m.pi/2, espace, 1)]

    parking[1].cutEnd(longueurPlace)

    eNew = m.sqrt(2) * largeurRoute
    thetaNew = parking[1].angle + (m.pi/4)
    newPos = pc.positionFin(parking[1])
    coinAireUnX, coinAireUnY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)

    testRoute = pc.Route(parking[1], longueurOpti, largeurRoute, -m.pi/2, espace, 'gauche')
    nbNewRoute = 0
    carla = testRoute.valide
    while carla:
        parking += [testRoute]
        nbNewRoute += 1
        testRoute = pc.Route(testRoute, longueurOpti, largeurRoute, 0, espace, 'gauche')
        carla = testRoute.valide

    routeDispo = [None,None,None]
    aireDispo = [0,0,0]
    nbRoute = [0,0,0]

    for i in range(2,nbNewRoute + 2):
        newRoute = pc.maxRoad(parking[i], largeurRoute, -m.pi/2, espace, 0.1)
        newRoute.cutEnd(longueurPlace)
        if not(newRoute.valide) :
            continue
        newPos = pc.positionFin(newRoute)
        thetaNew = newRoute.angle + (m.pi/4)
        coinAireDeuxX, coinAireDeuxY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)
        points = [(coinAireUnX, coinAireUnY), (coinAireUnX, coinAireDeuxY), (coinAireDeuxX, coinAireDeuxY), (coinAireDeuxX, coinAireUnY), (coinAireUnX, coinAireUnY)]
        carrePot = shapely.geometry.Polygon(points)
        notPossible = not(pc.inEspaceDeTravail(carrePot, espace.forme))
        while notPossible and newRoute.longueur > (longueurOpti*2):
            newRoute.cutEnd(largeurPlace)
            newPos = pc.positionFin(newRoute)
            thetaNew = newRoute.angle + (m.pi/4)
            coinAireDeuxX, coinAireDeuxY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)
            points = [(coinAireUnX, coinAireUnY), (coinAireUnX, coinAireDeuxY), (coinAireDeuxX, coinAireDeuxY), (coinAireDeuxX, coinAireUnY), (coinAireUnX, coinAireUnY)]
            carrePot = shapely.geometry.Polygon(points)
            notPossible = not(pc.inEspaceDeTravail(carrePot, espace.forme))
        if notPossible :
            continue
        airePot = carrePot.area
        if airePot < aireDispo[2] :
            continue
        if airePot > aireDispo[0] :
            routeDispo = [newRoute, routeDispo[0], routeDispo[1]]
            aireDispo = [airePot, aireDispo[0], aireDispo[1]]
            nbRoute = [i - 1, nbRoute[0], nbRoute[1]]
        elif airePot < aireDispo[1] :
            routeDispo = [routeDispo[0], newRoute, routeDispo[1]]
            aireDispo = [aireDispo[0], airePot, aireDispo[1]]
            nbRoute = [nbRoute[0], i - 1, nbRoute[1]]
        else : 
            routeDispo = [routeDispo[0], routeDispo[1], newRoute]
            aireDispo = [aireDispo[0], aireDispo[1], airePot]
            nbRoute = [nbRoute[0], nbRoute[1], i - 1]
        
    parkinglist = [parking.copy(), parking.copy(), parking.copy()]

    for i in range(3):
        if not(routeDispo[i]):
            continue 
        long0 = routeDispo[i].longueur
        long1 = long0 - parkinglist[i][1].longueur
        parkinglist[i] += [pc.Route(parkinglist[i][0], long1, largeurRoute, -m.pi/2, espace)]
        for j in range(2, nbRoute[i] + 2 ):
            parkinglist[i] += [pc.Route(parkinglist[i][j], long0, largeurRoute, -m.pi/2, espace)]
        print(parkinglist[i][-1])
        parkinglist[i] += [pc.Route(parkinglist[i][-1], nbRoute[i] * longueurOpti, largeurRoute, -m.pi/2, espace, 'gauche')]
        for j in range(nbRoute[i] + 2, nbNewRoute+2):
            parkinglist[i][j].valide = False
        parkinglist[i] = pc.remplissagePlace(parkinglist[i], longueurPlace, largeurPlace, espace)

    iMax = 0
    nbMaxPlace = pc.nbPlace(parkinglist[0])
    for i in range(1,3):
        if not(routeDispo[i]):
            continue 
        nbP = pc.nbPlace(parkinglist[i])
        if nbP > nbMaxPlace :
            nbMaxPlace = nbP
            iMax = i

    return parkinglist[iMax]


parking = remplissageAutoParkingStandart2(espace, rampe, 5, 5, 2.5)

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
