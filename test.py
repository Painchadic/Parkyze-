import parkyzeClass as pc
import shapely.geometry
import matplotlib.pyplot as py

espace = pc.EspaceDeTravail([(-20,-132), (-20,20), (30,20), (30,-32), (-20,-132)])
a,b,c,d = pc.camera(espace)
long = int(b - a) + 1
grid = [[0 for i in range(long)] for j in range(long)]
gridBot = [[0 for i in range(long)] for j in range(long)]
gridRight = [[0 for i in range(long)] for j in range(long)]
""" s = [[0 for i in range(long)] for j in range(long)] """

for i in range(long):
    for j in range(long):
        square = shapely.geometry.Polygon([(a + i, c + j),(a + i + 1, c + j),(a + i + 1, c + j + 1),(a + i, c + j + 1),(a + i, c + j)])       
        grid[i][j] = espace.forme.contains(square)
        """ s[i][j] = square """

for i in range(long - 1, -1, -1):
    for j in range(long - 1, -1, -1):
        if not(grid[i][j]):
            gridBot[i][j] = -1
            gridRight[i][j] = -1
            continue
        gridBot[i][j] = gridBot[i][j+1] + 1 
        gridRight[i][j] = gridRight[i+1][j] + 1
    
botMax = gridBot[0][0]
aireMax = botMax
colonneMax = 1
ligneMax = botMax
coord = (0,0)
for i in range(long):
    for j in range(long):
        if (grid[i][j]):

            botMax = gridBot[i][j]
            for k in range(gridRight[i][j]):
                if gridBot[i+k][j] < botMax :
                    botMax = gridBot[i+k][j]

                if aireMax < (k+1)*botMax:
                    aireMax = (k+1)*botMax
                    colonneMax = (k+2)
                    ligneMax = botMax+1
                    coord = (i,j)

""" for i in range(long):
    st = ""
    for j in range(long):
        st += str(gridBot[i][j])
        if j != long-1:
            st += ","
    print(st)

for i in range(long):
    st = ""
    for j in range(long):
        st += str(gridRight[i][j])
        if j != long-1:
            st += ","
    print(st) """

""" for i in range(long):
    for j in range(long):
        resX1, resY1 = s[i][j].exterior.xy
        if grid[i][j]:
            py.fill(resX1,resY1, color = 'r')
        py.plot(resX1,resY1, color = 'r') """

rectMax = [(a + coord[0], c + coord[1]), (a + coord[0] + colonneMax, c + coord[1]), (a + coord[0] + colonneMax, c + coord[1] + ligneMax), (a + coord[0], c + coord[1] + ligneMax), (a + coord[0], c + coord[1])]
rectMax = shapely.geometry.Polygon(rectMax)

resX, resY = espace.forme.exterior.xy
py.fill(resX,resY, color = espace.color)

resX0, resY0 = rectMax.exterior.xy
py.fill(resX0,resY0, color = 'b')

py.xlim(a,b)
py.ylim(c,d)
py.show()