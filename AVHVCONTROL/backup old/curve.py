from math import sin, cos, pi

curveCenter = [12,12]
radius = 10
degree=12

pos = [0,0]


pos[0] = curveCenter[0] + radius * (sin(1.5 * pi + degree))
pos[1] = curveCenter[1] + radius * (cos(1.5 * pi + degree))

print(pos)