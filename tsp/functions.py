
import math
from collections import namedtuple
import matplotlib.pyplot as plt
import random

Point = namedtuple("Point", ['x', 'y'])

__PLOT = False

def plot(solution, points, nodeCount):
    x = []
    y = []
    for index in range(nodeCount):
        x.append(points[solution[index]].x)
        y.append(points[solution[index]].y)
        plt.plot(x, y, 'xb-')
    plt.show()

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def tourLength(solution, points, nodeCount):
    l = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        l += length(points[solution[index]], points[solution[index+1]])
    return l