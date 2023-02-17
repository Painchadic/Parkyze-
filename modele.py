import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry

def remplissageAutoParkingStandart1(parking, largeurRoute, longueurPlace, largeurPlace, angleTest = m.pi/2):
    longueurOpti = largeurRoute + 2*longueurPlace


    angle = 0
    lon = 0
    while lon < longueurOpti + longueurPlace and angle < 7:
        tmp = pc.maxRoad(parking.rampe, largeurRoute, angle, parking.espace, 0.1)
        lon = tmp.longueur
        angle += angleTest
    
    if lon < longueurOpti + longueurPlace :
        if angleTest > m.pi/5 :
            remplissageAutoParkingStandart1(parking, largeurRoute, longueurPlace, largeurPlace, angleTest = m.pi/10)
        else : 
            Exception("Pas de possibilité")

    parking.addRoute(tmp)
    for i in np.arange(0, lon, longueurOpti):
        parking.addRoute(pc.maxRoad(tmp, largeurRoute, m.pi/2, parking.espace, 1, i))
        parking.addRoute(pc.maxRoad(tmp, largeurRoute, -m.pi/2, parking.espace, 1, i))

    parking.remplissagePlace(longueurPlace, largeurPlace)

    return 1

def remplissageAutoParkingStandart2(parking, largeurRoute, longueurPlace, largeurPlace):
    longueurOpti = largeurRoute + 2*longueurPlace

    parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, m.pi/2, parking.espace, 1))

    parking.routes[0].cutEnd(longueurPlace)

    aba = parking.routes[0].longueur
    a = aba%longueurOpti

    parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, -m.pi/2, parking.espace, 1))
        
    for i in np.arange(a, 0, -longueurOpti):
        lngRestant = i
        parking.addRoute(pc.maxRoad(parking.routes[0], largeurRoute, -m.pi/2, parking.espace, 1, i))

    for i in np.arange(longueurOpti - lngRestant, parking.routes[1].longueur, longueurOpti):
        parking.addRoute(pc.maxRoad(parking.routes[1], largeurRoute, m.pi/2, parking.espace, 1, i))

    parking.remplissagePlace(longueurPlace, largeurPlace)
    return 1

def remplissageAutoParkingStandart3(parking : pc.Parking, largeurRoute, longueurPlace, largeurPlace):
    longueurOpti = largeurRoute + 2*longueurPlace

    parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, m.pi/2, parking.espace, 1))

    parking.routes[0].cutEnd(longueurPlace)

    eNew = m.sqrt(2) * largeurRoute
    thetaNew = parking.routes[0].angle + (m.pi/4)
    newPos = pc.positionFin(parking.routes[0])
    coinAireUnX, coinAireUnY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)

    testRoute = pc.Route(parking.routes[0], longueurOpti, largeurRoute, -m.pi/2, parking.espace, 'gauche')
    nbNewRoute = 0
    carla = testRoute.valide
    while carla:
        nbNewRoute += 1
        testRoute.addEnd(longueurOpti, parking.espace)
        carla = testRoute.valide
    testRoute.cutEnd(longueurOpti)
    testRoute.valide = True
    parking.addRoute(testRoute)

    routeDispo = [False,False,False]
    aireDispo = [0,0,0]
    nbRoute = [0,0,0]

    for i in range(nbNewRoute):
        newRoute = pc.maxRoad(parking.routes[1], largeurRoute, -m.pi/2, parking.espace, 0.1, i*longueurOpti)
        newRoute.cutEnd(longueurPlace)

        cut = (newRoute.longueur - 2*largeurRoute) % largeurPlace
        newRoute.cutEnd(cut)

        if not(newRoute.valide) :
            continue

        newPos = pc.positionFin(newRoute)
        thetaNew = newRoute.angle + (m.pi/4)
        coinAireDeuxX, coinAireDeuxY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)
        points = [(coinAireUnX, coinAireUnY), (coinAireUnX, coinAireDeuxY), (coinAireDeuxX, coinAireDeuxY), (coinAireDeuxX, coinAireUnY), (coinAireUnX, coinAireUnY)]
        carrePot = shapely.geometry.Polygon(points)
        notPossible = not(pc.inEspaceDeTravail(carrePot, parking.espace.forme))
        while notPossible and newRoute.longueur > (longueurOpti*2):
            newRoute.cutEnd(largeurPlace)
            newPos = pc.positionFin(newRoute)
            thetaNew = newRoute.angle + (m.pi/4)
            coinAireDeuxX, coinAireDeuxY = newPos[0] + eNew * m.cos(thetaNew), newPos[1] + eNew * m.sin(thetaNew)
            points = [(coinAireUnX, coinAireUnY), (coinAireUnX, coinAireDeuxY), (coinAireDeuxX, coinAireDeuxY), (coinAireDeuxX, coinAireUnY), (coinAireUnX, coinAireUnY)]
            carrePot = shapely.geometry.Polygon(points)
            notPossible = not(pc.inEspaceDeTravail(carrePot, parking.espace.forme))
        if notPossible :
            continue
        airePot = carrePot.area
        if airePot < aireDispo[2] :
            continue
        if airePot > aireDispo[0] :
            routeDispo = [newRoute, routeDispo[0], routeDispo[1]]
            aireDispo = [airePot, aireDispo[0], aireDispo[1]]
            nbRoute = [i + 2, nbRoute[0], nbRoute[1]]
        elif airePot < aireDispo[1] :
            routeDispo = [routeDispo[0], newRoute, routeDispo[1]]
            aireDispo = [aireDispo[0], airePot, aireDispo[1]]
            nbRoute = [nbRoute[0], i + 2, nbRoute[1]]
        else : 
            routeDispo = [routeDispo[0], routeDispo[1], newRoute]
            aireDispo = [aireDispo[0], aireDispo[1], airePot]
            nbRoute = [nbRoute[0], nbRoute[1], i + 2]
        
    print(routeDispo)
    parkinglist = [parking.copy(), parking.copy(), parking.copy()]

    for i in range(3):
        if not(routeDispo[i]):
            continue 
        long0 = routeDispo[i].longueur
        long1 = long0 - parkinglist[i].routes[0].longueur
        parkinglist[i].addRoute(pc.Route(parkinglist[i].rampe, long1, largeurRoute, -m.pi/2, parking.espace))
        for j in range(1,nbRoute[i]):
            parkinglist[i].addRoute(pc.Route(parkinglist[i].routes[1], long0, largeurRoute, -m.pi/2, parking.espace, pospere = ((j)*longueurOpti)))
        parkinglist[i].addRoute(pc.Route(parkinglist[i].routes[2], (nbRoute[i]-1) * longueurOpti, largeurRoute, m.pi/2, parking.espace, 'droite'))
        parkinglist[i].remplissagePlace(longueurPlace, largeurPlace)

    iMax = 0
    nbMaxPlace = parkinglist[0].nbPlace()
    for i in range(1,3):
        if not(routeDispo[i]):
            continue 
        nbP = parkinglist[i].nbPlace()
        if nbP > nbMaxPlace :
            nbMaxPlace = nbP
            iMax = i

    return parkinglist[iMax]

def remplissageAutoParkingStandart4(parking : pc.Parking, largeurRoute, longueurPlace, largeurPlace):
    longueurOpti = largeurRoute + 2*longueurPlace

    parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, m.pi/2, parking.espace, 1))

    parking.routes[0].cutEnd(longueurPlace)
    
    parking.addRoute(pc.maxRoad(parking.routes[0], largeurRoute, -m.pi/2, parking.espace, 1))

    parking.routes[1].cutEnd(longueurPlace)

    newRoute = pc.Route(parking.routes[1], longueurOpti, largeurRoute, -m.pi/2, parking.espace, 'gauche')

    carla = newRoute.valide
    ind = -1
    where = 'droite'

    while carla:
        parking.addRoute(newRoute)

        road = pc.maxRoad(parking.routes[-1], largeurRoute, m.pi/2 * ind, parking.espace, 1)
        carlos = pc.geneRoute(road, (parking.routes + [parking.rampe]))

        while carlos and road.valide:
            road.cutEnd(largeurPlace)
            carlos = pc.geneRoute(road, (parking.routes + [parking.rampe]))

        road.cutEnd(longueurPlace)
        parking.addRoute(road)

        ind *= -1

        newRoute = pc.Route(parking.routes[-1], longueurOpti, largeurRoute, ind * m.pi/2, parking.espace, where)

        if where == 'droite':
            where = 'gauche'
        else:
            where = 'droite'

        carla = newRoute.valide

    parking.routes[-1].addEnd(largeurPlace, parking.espace)

    parking.remplissagePlace(longueurPlace, largeurPlace)

    return 1