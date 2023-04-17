import matplotlib.pyplot as py
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry
import random

def remplissageAutoParkingStandart1(parking, largeurRoute, longueurPlace, largeurPlace, angleTest = m.pi/2):
    longueurOpti = largeurRoute + 2*longueurPlace


    angle = 0
    lon = 0
    while lon < longueurOpti + longueurPlace and angle < 7:
        tmp = pc.maxRoad(parking.rampe, largeurRoute, angle, parking.espace, 0.1, limi = True)
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

def remplissageAleatoire(parking : pc.Parking, largeurRoute : float, longueurPlace : float, largeurPlace : float) :
    listAvailable = [(-1,i) for i in range(3)]
    remplissageAleatoireAux(parking, largeurRoute, longueurPlace, largeurPlace, listAvailable)
    parking.remplissagePlace(longueurPlace, largeurPlace)
    return 0

def remplissageAleatoireAux(parking : pc.Parking, largeurRoute : float, longueurPlace : float, largeurPlace : float, listAvailable):
    listAngle = [0, m.pi/2, -m.pi/2]
    if parking.espace_dispo() <= 0.75:
        return 0
    longueur = len(listAvailable)
    index = random.randint(0, longueur - 1)
    random_len = random.randint(1, 3)
    random_road = random.randint(0, 1)
    route, angle = listAvailable[index]
    angle = listAngle[angle]
    if route != -1:
        angle_difference = (parking.routes[route].pere.angle *180 )/ m.pi - angle *180 / m.pi
    else : 
        angle_difference = 90

    if route == -1:
        routeP = parking.rampe
    else :
        routeP = parking.routes[route]

    if random_road==0:
        maxroadtemp= pc.maxRoad(routeP, largeurRoute, angle, parking.espace, 1)
    else :
        if not (abs(angle_difference) % 180 <= 10) :
            maxroadtemp=pc.Route(routeP, random_len*15, largeurRoute, angle, parking.espace)
        else :
            print(angle_difference) 
            maxroadtemp=pc.Route(routeP, 15, largeurRoute, angle, parking.espace)
    
    maxroadtemp.cutEnd(longueurPlace)
    parking.addRoute(maxroadtemp)
    espacedispo = parking.espace_dispo()
    listAvailable.pop(index)
    listAvailable += [(len(parking.routes) - 1, i) for i in range(1,3)]
    return remplissageAleatoireAux(parking, largeurRoute, longueurPlace, largeurPlace, listAvailable)


def remplissageAutomatique2(parking : pc.Parking, largeurRoute : float, longueurPlace : float, largeurPlace : float, generations = 10, nombreDeFils = 5, nombreDeSurvivant = 2):
    parking.remplissagePlace(longueurPlace, largeurPlace)
    listParking = [parking]
    listScore = [0]
    return remplissageAutomatiqueAux2(listParking, listScore, largeurRoute, longueurPlace, largeurPlace, generations, nombreDeFils, nombreDeSurvivant)

def remplissageAutomatiqueAux2(listParking, listScore, largeurRoute : float, longueurPlace : float, largeurPlace : float, generations, nombreDeFils, nombreDeSurvivant):

    if generations == 0:
        max = listScore[0]
        index = 0
        for i in range(1, len(listScore)):
            if max < listScore[i] :
                max = listScore[1]
                index = i
        par = listParking[index]
        par.remplissagePlace(longueurPlace, largeurPlace)
        print(max)
        return par
    
    print(listScore)

    listParkingTMP = []
    listScoreTMP = []
    j = 0
    for parking in listParking :
        listParkingTMP += [parking.copy()]
        listScoreTMP += [listScore[j]]
        j += 1
        changements = []
        for i in range(nombreDeFils):
            parkingTMP = parking.copy()
            scoreTMP, changementTMP = mutation(parkingTMP, largeurRoute, longueurPlace, largeurPlace)
            if changementTMP in changements :
                continue
            listParkingTMP += [parkingTMP]
            listScoreTMP += [scoreTMP]
            changements += [changementTMP]

    while len(listParkingTMP) > nombreDeSurvivant:
        min_index = listScoreTMP.index(min(listScoreTMP))
        listScoreTMP.pop(min_index)
        listParkingTMP.pop(min_index)

    return remplissageAutomatiqueAux2(listParkingTMP, listScoreTMP, largeurRoute, longueurPlace, largeurPlace, generations - 1, nombreDeFils, nombreDeSurvivant)

def mutation(parking : pc.Parking, largeurRoute : float, longueurPlace, largeurPlace):
    
    scenario = random.randint(1,3)

    match scenario:
        # Route qui va jusqu'au fond
        case 1:
            route = random.randint(-1, len(parking.routes) - 1)
            direction = random.randint(0,2)
            if route == -1 :
                match direction :
                    case 0 :
                        parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, 0, parking.espace, 1))
                        changement = 'MaxRoad ' + 'Rampe ' + 'Devant'
                    case 1 :
                        parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, m.pi/2, parking.espace, 1))
                        changement = 'MaxRoad ' + 'Rampe ' + 'Gauche'
                    case 2 :
                        parking.addRoute(pc.maxRoad(parking.rampe, largeurRoute, -m.pi/2, parking.espace, 1))
                        changement = 'MaxRoad ' + 'Rampe ' + 'Droite'
            else :
                position = random.random() * parking.routes[route].longueur
                match direction :
                    case 0 :
                        parking.addRoute(pc.maxRoad(parking.routes[route], largeurRoute, 0, parking.espace, 1))
                        changement = 'MaxRoad ' + 'Route ' + str(route) + ' Devant'
                    case 1 :
                        parking.addRoute(pc.maxRoad(parking.routes[route], largeurRoute, m.pi/2, parking.espace, 1, position))
                        changement = 'MaxRoad ' + 'Route ' + str(route) + ' Gauche ' + str(position)
                    case 2 :
                        parking.addRoute(pc.maxRoad(parking.routes[route], largeurRoute, -m.pi/2, parking.espace, 1, position))
                        changement = 'MaxRoad ' + 'Route ' + str(route) + ' Droite ' + str(position)
        
        # Route qui va jusqu'au fond quasiment
        case 2:
            route = random.randint(-1, len(parking.routes) - 1)
            direction = random.randint(0,2)
            if route == -1 :
                match direction :
                    case 0 :
                        route = pc.maxRoad(parking.rampe, largeurRoute, 0, parking.espace, 1)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Rampe ' + 'Devant'
                    case 1 :
                        route = pc.maxRoad(parking.rampe, largeurRoute, m.pi/2, parking.espace, 1)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Rampe ' + 'Gauche'
                    case 2 :
                        route = pc.maxRoad(parking.rampe, largeurRoute, -m.pi/2, parking.espace, 1)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Rampe ' + 'Droite'
            else :
                position = random.random() * parking.routes[route].longueur
                match direction :
                    case 0 :
                        route = pc.maxRoad(parking.routes[route], largeurRoute, 0, parking.espace, 1)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Route ' + str(route) + ' Devant'
                    case 1 :
                        route = pc.maxRoad(parking.routes[route], largeurRoute, -m.pi/2, parking.espace, 1, position)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Route ' + str(route) + ' Gauche ' + str(position)
                    case 2 :
                        route = pc.maxRoad(parking.routes[route], largeurRoute, -m.pi/2, parking.espace, 1, position)
                        route.cutEnd(longueurPlace)
                        parking.addRoute(route)
                        changement = 'Quasi MaxRoad ' + 'Route ' + str(route) + ' Droite ' + str(position)
        
        # Route qui va +opti 

        case 3:
            long = longueurPlace*2 + largeurRoute + 0.2
            route = random.randint(-1, len(parking.routes) - 1)
            direction = random.randint(0,2)
            if route == -1 :
                match direction :
                    case 0 :
                        route = pc.Route(parking.rampe, long, largeurRoute, 0, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Rampe ' + 'Devant'
                    case 1 :
                        route = pc.Route(parking.rampe, long, largeurRoute, m.pi/2, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Rampe ' + 'Gauche'
                    case 2 :
                        route = pc.Route(parking.rampe, long, largeurRoute, -m.pi/2, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Rampe ' + 'Droite'
            else :
                position = random.random() * parking.routes[route].longueur
                match direction :
                    case 0 :
                        route = pc.Route(parking.routes[route], long, largeurRoute, 0, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Route ' + str(route) + ' Devant'
                    case 1 :
                        route = pc.Route(parking.routes[route], long, largeurRoute, -m.pi/2, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Route ' + str(route) + ' Gauche ' + str(position)
                    case 2 :
                        route = pc.Route(parking.routes[route], long, largeurRoute, -m.pi/2, parking.espace)
                        parking.addRoute(route)
                        changement = 'Longueur opti ' + 'Route ' + str(route) + ' Droite ' + str(position)

    placeP = parking.copy()
    placeP.remplissagePlace(longueurPlace, largeurPlace)
    score = (placeP.espace_dispo() * (parking.espace.forme.area / ((longueurPlace * largeurPlace * 2) + (largeurPlace * largeurRoute * 2)))) + placeP.nbPlace()
    return (score, changement)