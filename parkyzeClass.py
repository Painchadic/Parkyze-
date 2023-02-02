import math as m
import shapely.geometry

class ParkingTree :

    def __init__(self, p):
        self.pere = p
        self.fils = []

    def addFils(self, pt):
        self.fils += [pt]

class Route(ParkingTree) :
    def __init__(self, p, l, lar, a, edt, lim = False):
        super().__init__(p)
        self.longueur = l
        self.largeur = lar
        self.angle = a 
        self.limite = lim
        self.position = [0,0]
        if p != False :
            self.angle = a + p.angle
            self.position = positionFin(p)
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)
        if edt != 1:
            self.valide = inEspaceDeTravail(self.forme, edt.forme)
        else :
            self.valide = True
            
        if self.valide:
            if p != False :
                p.fils += [self]
        self.color = 'k'
        

    def __str__(self) -> str:
        x = "Route qui va de [" + str(self.position[0]) + ";" + str(self.position[1]) + "] à [" + str(positionFin(self)[0]) + ";" + str(positionFin(self)[1]) + "]."
        return x

    def cut(self, a : float):

        
        l = self.longueur
        self.longueur = a
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)

        secondeRoute = Route(self, l - a, self.largeur, 0, 1)
        return secondeRoute

    def turn(self, a : float):

        self.angle += a
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)

        return(1)

    def copy(self, edt):
        route = Route(False, self.longueur, self.largeur, self.angle, edt)
        route.position = self.position
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], route.angle)
            points[i][0] += route.position[0]
            points[i][1] += route.position[1]
        route.forme = shapely.geometry.Polygon(points)
        return route
    
    def cutEnd(self, a:float) :

        self.longueur -= a
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)
        if self.longueur < 0 :
            self.valide = False

    

class Noyaux(ParkingTree) :
    forme = []
    distanceRoute = 0

    def __init__(self, li, f):
        self.forme = shapely.geometry.Polygon(f)
        self.distanceRoute, p = closestRoute(self.forme, li)
        super().__init__(p)
        self.color = 'g'

    def valid(self, limite) :
        return (self.distanceRoute <= limite)

    def __str__(self):
        x = "Noyau en " + str(self.forme.centroid.xy[0][0]) + ";" + str(self.forme.centroid.xy[1][0]) + "]."
        return x


class Rampe(Route) :
    def __init__(self, l, lar, pos, a, h):
        if h/l > 0.18 :
            raise Exception("Rampe trop courte")
        super().__init__(False, l, lar, a, 1)
        self.position = pos
        self.hauteur = h
        self.color = 'r'
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)

    def __str__(self):
        x = "Rampe qui va de [" + str(self.position[0]) + ";" + str(self.position[1]) + "] à [" + str(positionFin(self)[0]) + ";" + str(positionFin(self)[1]) + "]."
        return x

    def vefifRampe(self) :
        res = True
        for k in self.fils:
            if type(k) != Route :
                res = False
                break
        return res

class Place(ParkingTree) :
    def __init__(self, p, l, lar, pos, a, edt):
        super().__init__(p)
        self.longueur = l 
        self.largeur = lar
        self.pos = pos
        self.position = [p.position[0] + m.cos(p.angle) * pos,p.position[1] + m.sin(p.angle) * pos]
        if a == 'gauche' :
            self.angle = p.angle + m.pi/2
        elif a == 'droite' :
            self.angle = p.angle - m.pi/2
        else :
            raise Exception("Mauvais 5e argument, soit droite soit gauche") 
        self.color = 'c'
        points = [(self.pere.largeur / 2, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, - self.largeur / 2), (self.pere.largeur / 2, - self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)
        self.valide = inEspaceDeTravail(self.forme, edt.forme)
        if self.valide :
            p.fils += [self]

    def __str__(self):
        x = "Place en " + str(self.forme.centroid.xy[0][0]) + ";" + str(self.forme.centroid.xy[1][0]) + "]."
        return x

class EspaceDeTravail :
    def __init__(self, f):
        self.forme = shapely.geometry.Polygon(f)
        self.color = 'y'

def positionA(e, d) :
    if d > e.longueur:
        raise Exception("Distance trop grande")
    return [e.position[0] + m.cos(e.angle)*d, e.position[1] + m.sin(e.angle)*d]

def positionFin(e) :
    return positionA(e, e.longueur)

def rotationAlpha(pos, a) :
    res = [0,0]
    res[0] = pos[0] * m.cos(a) - pos[1] * m.sin(a)
    res[1] = pos[0] * m.sin(a) + pos[1] * m.cos(a)
    return res

def closestRoute(f, r) -> Route:
    #Trouve la route la plus proche du Noyaux
    res = 1000
    route = r[0]
    for i in r :
        if type(i) != Route :
            continue
        tmp = min(res, f.exterior.distance(i.forme))
        if res <= tmp :
            continue
        res = tmp
        route = i
    return res, route


def distToRoad(f, r, res) -> float:
    # Distance To point1 r
    for i in range(len(f) - 1) :
        res = min(res, distSeg(f[i], f[i+1], r.position))
    # Distance To point2 r
    fin = positionFin(r)
    for i in range(len(f) - 1) :
        res = min(res, distSeg(f[i], f[i+1], fin))
    # Distance To points f
    for i in range(len(f)) :
        res = min(res, distSeg(r.position, fin, f[i]))
    return res

def distP(a,b) -> float:#distance entre deux points
    d=m.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
    return d
def distSeg(A,B,p) -> float:# le segment AB et le point p
    # A different de B
    if (A==B):
        dist=distP(A,p)
        pp=A
    if (A!=B): # calcule de la projection (pp)
        #Droite(AB)
        if ((B[0]-A[0])!=0):
            a1=(B[1]-A[1])/(B[0]-A[0]) #pente qui est la tangente
        else:
            a1=m.tan(m.pi/2) #infini, comme python donne une grande valeur au lieu d'une erreur on utilise tan(pi/2) sinon il suffit de mettre une tres grande valeur
        b1=A[1]-(a1*A[0]) #equation de droite y=ax+b
        #Droite(p,pp)
        if (a1!=0):
            a2=-1/a1 #les deux droites sont perpendiculaires
        else:
            a2=m.tan(m.pi/2) #infini
        b2=p[1]-(a2*p[0])
        #intersection pour trouver pp la projection
        x=(b2-b1) /(a1-a2) # (a1x+b1=a2x+b2) et (a1!=a2 car a1=-1/a1)
        y=a1*x+b1 # formule de droite y=ax+b
        pp=[x,y]
        if (distP(A,pp)<distP(A,B)) and (distP(B,pp)<distP(A,B)):# p dans la bande meme s'il est dans le segment
            dist=distP(p,pp)# pp reste comme il est
        else: #p hors de la bande
            if distP(A,pp)<distP(B,pp):#si cote de A
                dist=distP(A,p)
                pp=A
            else:# sinon cote de B
                dist=distP(B,p)
                pp=B
    return dist

def gene(n, li, lim):
    #vérifie si un élément du parking empiete sur l'élément n à lim m² près
    point1 = n.forme
    for j in li:
        if not(j.valide):
            continue
        point2 = j.forme
        if (n == j) :
            break
        a = point1.intersection(point2)
        if (a.area > lim): 
            if ((type(n) != Route and type(n) != Rampe) or (type(j) != Route and type(j) != Rampe)):
                return True, j
    return False, 'rien'

def geneRoute(n, p):
    point1 = n.forme
    for j in p:
        if not(j.valide):
            continue
        point2 = j.forme
        if (n == j) :
            break
        if (point1.intersects(point2)): 
            if (j != n.pere):
                return True
    return False

def inEspaceDeTravail(poly, e) -> bool:
    #Vérifie si le polynome poly est dans l'espace de travail
    if e.contains(poly) :
        return True
    return False

def camera(e):
    #Selon les dimensions de l'espace de travail, pose la camera 
    xmin, ymin, xmax, ymax = e.forme.bounds
    ecart = (xmax - xmin) - (ymax - ymin)
    ecart /= 2
    if ecart < 0 :
        ymax += 1
        ymin -= 1
        xmax += (1 - ecart)
        xmin -= (1 - ecart)
    else :
        xmax += 1
        xmin -= 1
        ymax += (1 + ecart)
        ymin -= (1 + ecart)

    return xmin, xmax, ymin, ymax

def remplissagePlace(parking, longueur, largeur, edt):
    #Ici on va parcourir toutes les routes afin de remplir tout esapce disponible en places
    for route in parking[::-1]:
        if type(route) != Route or not(route.valide):
            continue
        e = (largeur - route.largeur)/2
        if not(route.limite) or route.limite == 'droite':
            while e < route.longueur + route.largeur - 1.5*(largeur) :
                place = Place(route, longueur, largeur, e, 'droite', edt)
                probleme, cause = gene(n = place, li = parking, lim = 0.01)
                if not(probleme) :
                    if place.valide:
                        parking += [place]
                    e += largeur
                else : 
                    e = max((finProblem(cause, route, longueur) + largeur/2),e+0.1)

        if not(route.limite) or route.limite == 'gauche':
            e = (largeur - route.largeur)/2
            while e < route.longueur + route.largeur - 1.5*(largeur) :
                place = Place(route, longueur, largeur, e, 'gauche', edt)
                probleme, cause = gene(n = place, li = parking, lim = 0.01)
                if not(probleme) :
                    if place.valide:
                        parking += [place]
                    e += largeur
                else : 
                    e = max((finProblem(cause, route, longueur) + largeur/2),e+0.1)
    
    return parking

def finProblem(poly, route, longueur):
    points = [(-route.largeur / 2, route.largeur / 2 + longueur), (route.largeur / 2 + route.longueur, route.largeur / 2 + longueur), (route.largeur / 2 + route.longueur, - route.largeur / 2 - longueur), (-route.largeur / 2, - route.largeur / 2 - longueur), (-route.largeur / 2, route.largeur / 2 + longueur)]
    for i in range(len(points)):
        points[i] = rotationAlpha(points[i], route.angle)
        points[i][0] += route.position[0]
        points[i][1] += route.position[1]
    f = shapely.geometry.Polygon(points)
    test = f.intersection(poly.forme)
    xx, yy = test.exterior.xy
    coords = [[xx[i], yy[i]] for i in range(len(xx))]
    fin = 0
    for co in coords :
        fin = max(fin, (co[0] - route.position[0]) * m.cos(route.angle) + (co[1] - route.position[1]) * m.sin(route.angle))
    return fin

def nbPlace(parking) -> int:
    res = 0
    for e in parking :
        if type(e) == Place :
            res += 1
    return res

def ratio(parking, espace) -> float :
    return (espace.forme.area / nbPlace(parking))

def distSortie(rampe) -> float:
    return distSortieAux(rampe, 0)

def distSortieAux(route, longueurDuDebut) :
    res = 0
    for e in route.fils:
        if type(e) == Place :
            res = max(res, e.pos + longueurDuDebut)
        if type(e) == Route :
            res = max(res, distSortieAux(e, longueurDuDebut + route.longueur))
    return res

def maxRoad(p, lar, a, edt, lim):
    copyPere = p.copy(edt)
    xmin, ymin, xmax, ymax = edt.forme.bounds
    mini = 0
    maxi = max(xmax - xmin, ymax - ymin)

    while (maxi - mini) > lim:
        inter = (maxi + mini)/2
        tmpRoute = Route(copyPere, inter, lar, a, edt)
        if tmpRoute.valide:
            mini = inter
        else : 
            maxi = inter
        del tmpRoute
    return Route(p, mini, lar, a, edt)