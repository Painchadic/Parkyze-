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
        points = [(-self.largeur / 2, self.largeur / 2), (self.largeur / 2 + self.longueur, self.largeur / 2), (self.largeur / 2 + self.longueur, - self.largeur / 2), (-self.largeur / 2, - self.largeur / 2), (-self.largeur / 2, self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)
        self.color = 'k'

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
        self.position = [p.position[0] + m.cos(p.angle) * pos,p.position[1] - m.sin(p.angle) * pos]
        self.angle = p.angle + a
        self.color = 'c'
        points = [(self.pere.largeur / 2, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, self.largeur / 2), (self.pere.largeur / 2 + self.longueur, - self.largeur / 2), (self.pere.largeur / 2, - self.largeur / 2)]
        for i in range(len(points)):
            points[i] = rotationAlpha(points[i], self.angle)
            points[i][0] += self.position[0]
            points[i][1] += self.position[1]
        self.forme = shapely.geometry.Polygon(points)

class EspaceDeTravail :
    form = []

def positionFin(e) :
    return [e.position[0] + m.cos(e.angle)*e.longueur, e.position[1] - m.sin(e.angle)*e.longueur]

def rotationAlpha(pos, a) :
    res = [0,0]
    res[0] = pos[0] * m.cos(a) + pos[1] * m.sin(a)
    res[1] = - pos[0] * m.sin(a) + pos[1] * m.cos(a)
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
    for j in li :
        point2 = j.forme
        if (n == j) :
            break
        if (point1.intersection(point2).area > lim): 
            if ((type(n) != Route and type(n) != Rampe) or (type(j) != Route and type(j) != Rampe)):
                return True
    return False