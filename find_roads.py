import pandas as pd
import numpy as np

import math

from matplotlib import pyplot as plt
pd.set_option('display.max_colwidth', 10)

data = pd.read_csv("./data/train/roads_dataset.csv")

data_size = len(data["geometry"])
print(data)
lines = list()

for i in range(data_size):
    cords = data["geometry"][i][12:-1].split(", ")
    cords[0] = cords[0].split(' ')
    for j in range(1, len(cords)):
        cords[j] = cords[j].split(' ')
        lines.append([float(cords[j][0]), float(cords[j][1]), float(cords[j-1][0]), float(cords[j-1][1]), data["highway"][i], data["name"][i]])


def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z

def length(v):
    x,y,z = v
    return max(math.sqrt(x*x + y*y + z*z), 0.000000001)

def vector(b,e):
    x,y,z = b
    X,Y,Z = e
    return (X-x, Y-y, Z-z)

def unit(v):
    x,y,z = v
    mag = length(v)
    return (x/mag, y/mag, z/mag)

def distance(p0,p1):
    return length(vector(p0,p1))

def scale(v,sc):
    x,y,z = v
    return (x * sc, y * sc, z * sc)

def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)


def dist(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return dist


def get_roads(x, y, radius):
    roads = dict()
    cnt = 0
    x, y = y, x
    for line in lines:

        if not(line[5] in roads):
            if dist((x,y, 0), (line[0], line[1], 0), (line[2], line[3], 0)) < radius:
                roads[line[5]]=[line[4], line[5]]
    return roads.values()


def get_roads_value(x, y, types, radius=0.01): #recommended radius 0.01
    roads = get_roads(x, y, radius)
    answer = 0
    for i in roads:
        if i[0] in types:
            answer+=1
    return answer


if __name__ == '__main__':
    print(get_roads_value(59.93, 30.32, 0.01, "motorway"))