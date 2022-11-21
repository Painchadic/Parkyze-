import math as m
import shapely.geometry

class ParkingTree :

    def __init__(self, p):
        self.pere = p
        self.fils = []

    def addFils(self, pt):
        self.fils += [pt]

class Route(ParkingTree) :
    def __init__(self, p, l, lar, a):
        super().__init__(p)
        self.longueur = l
        self.largeur = lar
        self.angle = a 
        self.position = [0,0]
        if p != False :
            self.angle = a + p.angle
            self.position = positionFin(p)
            p.fils += [self]
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)
        self.color = 'k'

    def __str__(self):
        x = "Route qui va de [" + str(self.position[0]) + ";" + str(self.position[1]) + "] à [" + str(positionFin(self)[0]) + ";" + str(positionFin(self)[1]) + "]."
        return x

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
        super().__init__(False, l, lar, a)
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
    def __init__(self, p, l, lar, pos, a):
        super().__init__(p)
        self.longueur = l 
        self.largeur = lar
        self.position = [p.position[0] + m.cos(p.angle) * pos,p.position[1] + m.sin(p.angle) * pos]
        if a == 'gauche' :
            self.angle = p.angle + m.pi/2
        elif a == 'droite' :
            self.angle = p.angle - m.pi/2
        else :
            raise Exception("Désolé, soit droite soit gauche") 
        self.color = 'c'
        points = [(self.pere.largeur / 2, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, - self.largeur / 2), (self.pere.largeur / 2, - self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)

    def __str__(self):
        x = "Place en " + str(self.forme.centroid.xy[0][0]) + ";" + str(self.forme.centroid.xy[1][0]) + "]."
        return x

class EspaceDeTravail :
    def __init__(self, f):
        self.forme = shapely.geometry.Polygon(f)
        self.color = 'y'

def positionFin(e) :
    return [e.position[0] + m.cos(e.angle)*e.longueur, e.position[1] + m.sin(e.angle)*e.longueur]

def rotationAlpha(pos, a) :
    res = [0,0]
    res[0] = pos[0] * m.cos(a) - pos[1] * m.sin(a)
    res[1] = pos[0] * m.sin(a) + pos[1] * m.cos(a)
    return res

def closestRoute(f, r) :
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


def distToRoad(f, r, res) :
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

def distP(a,b):#distance entre deux points
    d=m.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
    return d
def distSeg(A,B,p):# le segment AB et le point p
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
    point1 = n.forme
    for j in li:
        point2 = j.forme
        if (n == j) :
            break
        if (point1.intersection(point2).area > lim): 
            if ((type(n) != Route and type(n) != Rampe) or (type(j) != Route and type(j) != Rampe)):
                return True, j
    return False, 'rien'

def inEspaceDeTravail(poly, e):
    tmp = poly.intersection(e)
    if (tmp.area + 0.01) < poly.area :
        return False
    return True

def camera(e):
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

def remplissagePlace(parking, longueur, largeur):
    #Ici on va parcourir toutes les routes afin de remplir tout esapce disponible en places
    places = []
    for route in parking:
        if type(route) != Route :
            continue
        e = (largeur - route.largeur)/2
        while e < route.longueur + route.largeur - largeur :
            place = Place(route, longueur, largeur, e, 'droite')
            probleme, cause = gene(place, parking, 0.01)
            if not(probleme) :
                parking += [place]
                e += largeur
            else : 
                e = finProblem(cause, route, longueur) + largeur/2

        e = (largeur - route.largeur)/2
        while e < route.longueur + route.largeur - largeur :
            place = Place(route, longueur, largeur, e, 'gauche')
            probleme, cause = gene(place, parking, 0.1)
            if not(probleme) :
                parking += [place]
                e += largeur
            else : 
                e = finProblem(cause, route, longueur) + largeur/2
    
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