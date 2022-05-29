import pandas as pd
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from matplotlib import path
import matplotlib.pyplot as plt
from collections import defaultdict

import math

data = pd.read_csv("./data/train/isochrones_walk_dataset.csv")
polygons = list()
data_size = len(data["walk_15min"])
for i in range(data_size):
    polygons.append([data["lat"][i], data["lon"][i], []])

    polygons[i][2] = [list(map(float, j.split(' '))) for j in data["walk_15min"][i][10:-2].split(', ')]


def distance(x1, y1, x2, y2):
    c = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return c


def find_closest_isochrone(x, y):
    closest = 0
    for i in range(data_size):
        dist0 = distance(x, y, polygons[closest][0], polygons[closest][1])
        dist1 = distance(x, y, polygons[i][0], polygons[i][1])
        if dist0>dist1:
            closest = i
    return polygons[closest]


def in_isochrone(x, y, polygon):
    if Polygon(polygon[2]).contains(Point(x, y)) or Polygon(polygon[2]).contains(Point(y, x)):
        return True
    else:
        return False
stops = pd.read_csv("./data/train/osm_stops.csv")


def find_stops(x, y):
    polygon = find_closest_isochrone(x, y)
    cnt = 0
    for i in range(len(stops["lat"])):
        if distance(x, y, stops["lat"][i], stops["lon"][i]) < 0.1:
            if in_isochrone(stops["lat"][i], stops["lon"][i], polygon):
                cnt+=1
    return cnt


objects = pd.read_csv("./data/train/osm_amenity.csv")


def find_objects(x, y):
    polygon = find_closest_isochrone(x, y)
    cnt = defaultdict(int)
    for i in range(len(objects["lat"])):
        if distance(x, y, objects["lat"][i], objects["lon"][i]) < 0.1:
            if in_isochrone(objects["lat"][i], objects["lon"][i], polygon):
                cnt["Авторемонт и техобслуживание (СТО)"] += objects["Авторемонт и техобслуживание (СТО)"][i]
                cnt["Банки"] += objects["Банки"][i]
                cnt["Быстрое питание"] += objects["Быстрое питание"][i]
                cnt["Доставка готовых блюд"] += objects["Доставка готовых блюд"][i]
                cnt["Женская одежда"] += objects["Женская одежда"][i]
                cnt["Кафе"] += objects["Кафе"][i]
                cnt["Овощи / Фрукты"] += objects["Овощи / Фрукты"][i]
                cnt["Рестораны"] += objects["Рестораны"][i]
                cnt["Супермаркеты"] += objects["Супермаркеты"][i]

    return cnt

if __name__ == '__main__':
    print(find_objects(59.935687, 30.327232))
    print(find_stops(59.935687, 30.327232))